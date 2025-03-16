# seeing if Istio can help...

## initially, attempted
sudo microk8s enable istio (having enabled community first)
### did ok, but some deployments and daemon sets failed.

### adjusted:
#### istio & loki, prom stack
sudo ufw allow 15021
sudo ufw allow 3101

### restarted
sudo microk8s stop; sudo microk8s start

## observability:
### loki prom stack daemon was deleted
so:
sudo microk8s disable observability
then:
sudo microk8s enable observability

# istio getting started guide:
https://istio.io/latest/docs/ambient/getting-started/


# running istioctl:
microk8s istioctl
- e.g.
microk8s istioctl x precheck


# installing via helm (matching microk8s version)
- clear first
k delete namespace istio-system

- helm install
microk8s helm install istio-base istio/base -n istio-system --set defaultRevision=1.18.2 --create-namespace

# installing operator:
microk8s istioctl operator init

# istio dashboards:
microk8s istioctl dashboard

Usage:
  istioctl dashboard [flags]
  istioctl dashboard [command]

Aliases:
  dashboard, dash, d

Available Commands:
  controlz    Open ControlZ web UI
  envoy       Open Envoy admin web UI
  grafana     Open Grafana web UI
  jaeger      Open Jaeger web UI
  kiali       Open Kiali web UI
  prometheus  Open Prometheus web UI
  skywalking  Open SkyWalking UI
  zipkin      Open Zipkin web UI

-- need to enable services first

# istio CNI
helm install istio-cni istio/cni -n istio-system --set profile=ambient --set global.platform=microk8s --wait
- worked


# kiali 1.24
k apply -f https://raw.githubusercontent.com/istio/istio/release-1.24/samples/addons/kiali.yaml
