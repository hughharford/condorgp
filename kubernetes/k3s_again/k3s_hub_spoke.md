# k3s hub-and-spoke over the internet

Guide for the secure hub (server) and spokes (agents) setup. Topics use the letters from the
review so they can be referred to directly: **F** firewall, **G** kubeconfig, **B** join tokens.

Related: `k3s/` (config examples + `ufw_rules.sh`), `kubernetes/secrets_management.md`.

## 1. Hub

1. Copy `k3s/config.server.example.yaml` to `/etc/rancher/k3s/config.yaml` and fill in the placeholders.
2. Create the token files, readable by root only (**B**; see the secrets guide for why):
   ```bash
   sudo install -d -m 700 /etc/rancher/k3s
   sudo sh -c 'umask 077; openssl rand -hex 32 > /etc/rancher/k3s/server-token'
   sudo sh -c 'umask 077; openssl rand -hex 32 > /etc/rancher/k3s/agent-token'
   ```
3. Firewall first (**F**, section 4), then install:
   ```bash
   curl -sfL https://get.k3s.io | sudo sh -s - server
   ```
   Everything else comes from the config file, so no token or secret ends up in shell history.

## 2. Spokes

1. Copy `k3s/config.agent.example.yaml` to `/etc/rancher/k3s/config.yaml` and fill it in.
2. Put the hub's **agent** token into `/etc/rancher/k3s/agent-token` (mode 600). Transfer it with `scp`
   or a password manager, never by pasting it into chat, an issue or a commit.
3. Open the firewall (section 4), then `curl -sfL https://get.k3s.io | sudo sh -s - agent`.

## 3. Kubeconfig mode (G)

The hub writes `/etc/rancher/k3s/k3s.yaml` with cluster-admin credentials. It is written with mode
**0600** (`write-kubeconfig-mode: "0600"` in the server config). Never use 644: it lets every local
user on the hub read those credentials.

With a 0600 file, use kubectl like this:

- On the hub, as an admin: `sudo k3s kubectl get nodes`
- Or copy it into your own account (it is already yours alone):
  ```bash
  mkdir -p ~/.kube
  sudo install -m 600 -o "$USER" /etc/rancher/k3s/k3s.yaml ~/.kube/k3s.yaml
  export KUBECONFIG=~/.kube/k3s.yaml
  ```
- From your laptop: copy that file, set `server:` to `https://<HUB_PUBLIC_IP>:6443`, keep it 600.

`k3s.yaml` and `*.kubeconfig` are in `.gitignore`. Never commit them.

## 4. Firewall (F)

`k3s/ufw_rules.sh` prints (and with `APPLY=1` applies) rules where every inbound rule names a
source address. Dry-run first, read the output, then apply.

```bash
# on the hub
ROLE=hub   ADMIN_IP=<your public IP> NODE_IPS="<spoke1> <spoke2>" bash k3s/ufw_rules.sh
sudo ROLE=hub   ADMIN_IP=<your public IP> NODE_IPS="<spoke1> <spoke2>" APPLY=1 bash k3s/ufw_rules.sh
# on each spoke: ROLE=spoke, NODE_IPS = the hub and the other spokes
```

- SSH is allowed from `ADMIN_IP` only, and is added before default-deny. If your public IP changes you
  are locked out: keep console access to the machines (cloud console or a keyboard).
- 6443 (API) is open on the hub to the admin and the nodes only; spokes open no API port.
- 51820/51821 udp (WireGuard) and 10250 tcp (kubelet) are open to the nodes only.
- 8472/udp (Flannel VXLAN) is never opened; it is unencrypted.
- The two k3s pod/service networks (10.42.0.0/16, 10.43.0.0/16) are allowed, as the k3s docs advise.
- IPv4 only for now.

## 5. Checks

```bash
python -m pytest -m F_ufw -m G_kubeconfig   # or one at a time: -m F_ufw, -m G_kubeconfig
```
