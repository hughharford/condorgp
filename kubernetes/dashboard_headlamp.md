# Dashboard (Headlamp)

Replaces the retired Kubernetes Dashboard v2.7.0 (the MicroK8s `dashboard` addon installed that
version, so the addon is no longer enabled by the scripts).

Manifests: `k8s/11-headlamp.yaml` (namespace `headlamp`, pinned image, hardened pod, ClusterIP service)
and `k8s/12-dashboard-viewer.yaml` (read-only login account).

## Open it

    make k_dash      # microk8s: prints a 1 hour read-only token, port-forwards to localhost:4466
    make k3_dash     # k3s: same
    # then http://localhost:4466 and paste the token

From another machine use an SSH tunnel: `ssh -L 4466:localhost:4466 <host>`.

## Security (read before changing)

- The login user is READ-ONLY (the built-in `view` role: no Secrets, no writes). It is not cluster-admin.
- Headlamp calls the API with the token you paste at login. Its own pod account has no permissions at
  all, so a bug or leak in the UI itself gains nothing.
- The port-forward listens on localhost by default. Do not add `--address` to it, and never put the
  dashboard behind the Ingress (`k8s/08-ingress.yaml`).
- Tokens from `create token` expire after 1h. Do not create long-lived tokens or token Secrets for it.
- The image is pinned (v0.46.0) in `k8s/11-headlamp.yaml`. Upgrade by changing the tag after reading the release notes.
- Check it all with: `python -m pytest -m E_dashboard`

## Temporary admin access (only when you must change things from the UI)

    kubectl create serviceaccount dash-tmp-admin -n headlamp
    kubectl create clusterrolebinding dash-tmp-admin --clusterrole=cluster-admin --serviceaccount=headlamp:dash-tmp-admin
    kubectl -n headlamp create token dash-tmp-admin --duration=15m
    # ...do the work, then ALWAYS remove it:
    kubectl delete clusterrolebinding dash-tmp-admin
    kubectl delete serviceaccount dash-tmp-admin -n headlamp

(`kubectl` = `microk8s kubectl` or `k3s kubectl`.)

## Clean up the old dashboard on an existing cluster

    kubectl delete clusterrolebinding dashboard-admin --ignore-not-found
    kubectl delete serviceaccount dashboard-admin -n default --ignore-not-found
    # the retired Kubernetes Dashboard v2.7.0, if it is still installed (microk8s: also `microk8s disable dashboard`):
    kubectl delete namespace kubernetes-dashboard --ignore-not-found
    kubectl delete clusterrole,clusterrolebinding kubernetes-dashboard --ignore-not-found
