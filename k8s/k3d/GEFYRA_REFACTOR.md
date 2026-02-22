# K3d + Gefyra Refactoring Guide

## Summary of Issues Found

### 1. **Namespace vs connection name**

- `-n` in `gefyra connections connect` = **Kubernetes namespace** to bridge (where your workloads live).
- Use `cgp-system` to reach cgp-worker, cgp-master, etc.
- Override with `GEFYRA_NAMESPACE=cgp make k3d_gefyra` if you use a different namespace.

---

### 2. **Wrong API Server Port**

In `w_reg_n_api_reg_start_k3d.sh` and `gefyra_notes.md`:

```
kubectl config set-cluster k3d-cgp-cluster --server=https://127.0.0.1:46233
```

The cluster is created with `--api-port 6550`, so the API server should be `https://127.0.0.1:6550`. Port 46233 appears to be incorrect (possibly from an old or different setup).

---

### 3. **Port confusion: API (6550) vs WireGuard (31820)**

- **6550** = Kubernetes API server – used in kubeconfig (`--server`). Required for `kubectl` and the Gefyra CLI.
- **31820** = WireGuard UDP port – used in `gefyra clients config -p`. Required for the VPN tunnel.

Do not use 31820 as the API server port in kubeconfig.

---

### 4. **TLS verification failure** (SSL: CERTIFICATE_VERIFY_FAILED)

**Root cause:** k3s generates API server certs with SANs for internal hostnames (kubernetes.default, host.docker.internal), but not for `127.0.0.1` when accessed from the host. TLS hostname verification then fails.

**Proper fix:** Add `--tls-san` when creating the cluster so the cert includes 127.0.0.1 and localhost:

```bash
k3d cluster create ... --k3s-arg "--tls-san=127.0.0.1@server:0" --k3s-arg "--tls-san=localhost@server:0"
```

This is now in `w_reg_n_api_reg_start_k3d.sh`. TLS verification can remain enabled; no need for `insecure-skip-tls-verify`.

---

### 5. **Hardcoded Docker Gateway IP**

`apply_gefyra.sh` and `gefyra_notes.md` hardcode `-h 172.19.0.1`. The k3d Docker network gateway can vary (e.g. 172.17.0.1, 172.18.0.1). It should be discovered dynamically:

```bash
docker exec k3d-cgp-cluster-server-0 sh -lc "ip route | awk '/default/ {print \$3; exit}'"
```

---

### 6. **Inconsistent Cluster Creation Scripts**

You have multiple start scripts with different configurations:

| Script | Port 31820 | Load balancer | Notes |
|--------|------------|---------------|-------|
| w_reg_n_api_reg_start_k3d.sh | ✅ `-p 31820:31820/UDP@agent:1` | Uses agents | Gefyra-compatible |
| w_registry_reg_start_k3d.sh | ❌ Missing | Uses loadbalancer | Gefyra will fail |
| reg_start_k3d.sh | ❌ Missing | Uses loadbalancer | Gefyra will fail |

Gefyra requires port **31820/UDP** to be exposed. Only `w_reg_n_api_reg_start_k3d.sh` does this.

---

### 7. **Makefile `k3d_gefyra` Target**

```makefile
k3d_gefyra:
	@gefyra install | kubectl apply -f -
	@gefyra install --service-type=Loadbalancer
```

- The first line pipes the manifest to `kubectl apply` instead of letting `gefyra install` manage installation.
- The second line runs a second `gefyra install` with `--service-type=Loadbalancer` (for k3d you typically need LoadBalancer to reach the WireGuard service from the host).
- Use one correct install flow instead of two conflicting steps.

---

### 8. **Incomplete Gefyra Workflow in `apply_gefyra.sh`**

`apply_gefyra.sh` skips:

1. `gefyra install` (operator)
2. Client creation (`gefyra clients create`)
3. Dynamic gateway IP discovery

It only runs client config and connect. The full workflow should be ordered and documented.

---

### 9. **Gefyra Basic Workload Not in Main Apply**

`000-gefyra-basic-workload.yaml` is for testing (hello-nginx, bye-nginx) and is not applied by `apply_k3d.sh`. That’s acceptable, but the comment in `apply_gefyra.sh` suggests applying it. If you want Gefyra tests, it should be part of a documented or optional step.

---

### 10. **apply_k3d.sh Path Assumption**

`apply_k3d.sh` uses paths like `k8s/k3d/k3d_yaml/...` without `cd` to the repo root. If run from another directory it will fail. Either `cd` to repo root or use `$(git rev-parse --show-toplevel)` (or equivalent) at the start.

---

## Recommended Refactoring

### Fix 1: Unified Gefyra Setup Script

Create a single script that encapsulates the full Gefyra setup:

```bash
#!/bin/bash
# k8s/k3d/gefyra_setup.sh - Full Gefyra setup for k3d
set -e

KUBECONFIG_FILE="/tmp/gefyra-kubeconfig.yaml"
CLIENT_JSON="/tmp/gefyra-local.json"
CLIENT_ID="local"
NAMESPACE="cgp-system"

# 1. Ensure kubeconfig uses correct API server
kubectl config view --raw --minify > "$KUBECONFIG_FILE"
# Fix server URL if needed (use 6550, not 46233)
kubectl config set-cluster k3d-cgp-cluster --server=https://127.0.0.1:6550 --kubeconfig="$KUBECONFIG_FILE"

# 2. Install Gefyra operator
env -i HOME="$HOME" PATH="$PATH" KUBECONFIG="$KUBECONFIG_FILE" \
  gefyra install --apply --wait --service-type=LoadBalancer

# 3. Get Docker gateway (host IP from cluster's perspective)
GATEWAY_IP=$(docker exec k3d-cgp-cluster-server-0 sh -lc "ip route | awk '/default/ {print \$3; exit}'")
echo "Using gateway IP: $GATEWAY_IP"

# 4. Create and configure client
env -i HOME="$HOME" PATH="$PATH" KUBECONFIG="$KUBECONFIG_FILE" \
  gefyra clients create --client-id "$CLIENT_ID" 2>/dev/null || true

env -i HOME="$HOME" PATH="$PATH" KUBECONFIG="$KUBECONFIG_FILE" \
  gefyra clients config "$CLIENT_ID" -h "$GATEWAY_IP" -p 31820 -o "$CLIENT_JSON"

# 5. Connect
env -i HOME="$HOME" PATH="$PATH" KUBECONFIG="$KUBECONFIG_FILE" \
  gefyra connections connect -f "$CLIENT_JSON" -n "$NAMESPACE"

echo "Gefyra connected to namespace $NAMESPACE"
```

### Fix 2: Consolidate Cluster Start Scripts

Keep one canonical script (e.g. `w_reg_n_api_reg_start_k3d.sh`) that:

- Exposes 31820/UDP
- Sets API port 6550
- Regenerates the Gefyra kubeconfig with the correct server URL

### Fix 3: Update w_reg_n_api_reg_start_k3d.sh

```diff
- kubectl config set-cluster k3d-cgp-cluster --server=https://127.0.0.1:46233
+ kubectl config set-cluster k3d-cgp-cluster --server=https://127.0.0.1:6550
```

### Fix 4: Simplify Makefile

```makefile
k3d_gefyra:
	@sh k8s/k3d/gefyra_setup.sh

k3d_g_apply:
	@sh k8s/k3d/gefyra_setup.sh
```

(Or point both to the same script if you want identical behavior.)

### Fix 5: apply_k3d.sh – Work from Repo Root

```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

# ... rest of apply commands
```

---

## Quick Fix Checklist

- [x] Change all `-n cgp` to `-n cgp-system` ✅
- [x] Change API server port from 46233 to 6550 ✅
- [x] Add dynamic gateway IP discovery (replace hardcoded 172.19.0.1) ✅
- [x] Ensure only cluster start scripts that expose 31820/UDP are used for Gefyra ✅ (w_reg_n_api_reg_start_k3d.sh)
- [x] Fix or replace the `k3d_gefyra` Makefile target ✅
- [ ] Add `cd` to repo root (or equivalent) in `apply_k3d.sh` (optional - run from repo root)

---

## Debugging Gefyra

If it still fails:

1. **Check Gefyra operator**: `kubectl get pods -n gefyra`
2. **Check WireGuard service**: `kubectl get svc -A | grep gefyra`
3. **Verify port 31820**: `nc -zvu 127.0.0.1 31820` (UDP)
4. **Gefyra logs**: `gefyra connections list` and `gefyra clients list`
