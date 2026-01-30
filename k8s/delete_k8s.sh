# delete this set:

microk8s kubectl delete -f k8s/09-ingress.yaml
microk8s kubectl delete -f k8s/08-cgp-master.yaml
microk8s kubectl delete -f k8s/07-worker.yaml
microk8s kubectl delete -f k8s/06-grafana.yaml
microk8s kubectl delete -f k8s/05-rabbitmq.yaml
microk8s kubectl delete -f k8s/04-postgres.yaml
microk8s kubectl delete -f k8s/03-persistent-volumes.yaml
microk8s kubectl delete -f k8s/02-secrets.yaml
microk8s kubectl delete -f k8s/01-configmap.yaml
microk8s kubectl delete -f k8s/00-namespace.yaml
