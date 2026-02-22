# ----------------------------------
#          INSTALL
# ----------------------------------
install_requirements:
	@sudo pip install poetry==1.8.4
	@poetry install

install:
	@poetry install

fresh_install:
	@make install_requirements
	@make new_install
	@sh scripts/establish_logs_n_checkpoints.sh

new_install:
	@echo checking paths
	@sh scripts/checking_env.sh

update_env:
	@direnv allow

# # ----------------------------------
# #          Kubernetes - microk8s
# # ----------------------------------

# k8s_install_new:
# 	@zsh k8s/install_microk8s.sh;

# k8s_cgp_builds:
# 	@sudo DOCKER_BUILDKIT=1 docker build -f docker/Dockerfile_start_again --target=cgp-nt-again -t cgp-nt-again .

# k8s_reset_cgp:
# 	@sudo microk8s kubectl delete -f k8s/07-worker.yaml
# 	@sudo microk8s kubectl apply -f k8s/07-worker.yaml

# k8s_apply:
# 	@sudo sh k8s/k8s_apply.sh;

# k8s_delete:
# 	@sudo sh k8s/k8s_delete.sh;

# k8s_cgp_images:
# 	@sudo sh k8s/k8s_images_push.sh;

# k8s_forwarding:
# 	@microk8s kubectl port-forward service/cgp-grafana 3000:3000  -n cgp-system --request-timeout='0' &
# 	@microk8s kubectl port-forward service/cgp-rabbitmq 15672:15672  -n cgp-system --request-timeout='0' &
# 	@microk8s kubectl port-forward service/cgp-rabbitmq 5672:5672  -n cgp-system --request-timeout='0' &
# 	@microk8s kubectl port-forward service/cgp-database 5432:5432 -n cgp-system --request-timeout='0'  &

# k8s_st_start:
# 	@sudo sh k8s/reg_k8s_start.sh;

# k8s_sp_stop:
# 	@sudo microk8s stop;

# ----------------------------------
#          K8S with K3d and K3S
# ----------------------------------

k3d_shutdown:
	@gefyra down
	@k3d cluster stop cgp-cluster
	@k3d registry delete k3d-cgp-registry.localhost
	@k3d cluster delete cgp-cluster
	@k3d cluster stop k3s-default
	@k3d cluster delete k3s-default
	@docker network rm k3d-cgp-cluster
	@docker system prune -f
	@rm -f $(docker ps -af label=k3d.io -q)
	@sudo fuser -k 6550/tcp
	@sudo fuser -k 8080/tcp
	@sudo fuser -k 6443/tcp
	@sudo fuser -k 8443/tcp

k3d_gefyra:
	@sh k8s/k3d/gefyra_setup.sh

k3d_g_apply:
	@sh k8s/k3d/apply_gefyra.sh


k3d_out_config:
	@k3d kubeconfig get cgp-cluster > k8s/k3d/output-kube-config.yaml
	@export KUBECONFIG="$(k3d kubeconfig get cgpcluster-)"


k3d_full_reset:
	@sh k8s/k3d/w_reg_n_api_reg_start_k3d.sh
	@sh k8s/k3d/images_push_k3d.sh
	@sh k8s/k3d/apply_k3d.sh
	@make k3d_dash

k3d_del:
	@k3d cluster stop cgp-cluster
	@sh k8s/k3d/cluster_delete_k3d.sh

k3d_stop:
	@k3d cluster stop cgp-cluster

k3d_apply:
	@sh k8s/k3d/apply_k3d.sh

k3d_dash:
	@K3D_KUBECONFIG=/tmp/k3d-cgp-kubeconfig.yaml; sh k8s/k3d/dash_kubeconfig.sh

k3d_reset_cgp:
	@sh k8s/k3d/reset_worker_k3d.sh
	@sh k8s/k3d/reset_master_k3d.sh

# ----------------------------------
#          TEST
# ----------------------------------

check_code:
	@flake8 scripts/* condorgp/*.py

black:
	@black scripts/* condorgp/*.py

# tests/*.py
test:
	@PYTHONPATH=. pytest
	@coverage run -m pytest
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr condorgp-*.dist-info
	@rm -fr condorgp.egg-info



all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)
