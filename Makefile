# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@sudo pip install poetry
	@poetry install

check_code:
	@flake8 scripts/* condorgp/*.py

black:
	@black scripts/* condorgp/*.py

# K3S Commands:
# #############################################################################
k3_stop:
	sudo systemctl stop k3s;

k3_start:
	sudo systemctl start k3s;

k3_status:
	systemctl status k3s;

k3_server_etc:
	sudo k3s server;
	sudo k3s agent;

k3_kubectl:
	k3s kubectl;

k3_kapply:
	k3s kubectl apply -f k8s/00-namespace.yaml
	k3s kubectl apply -f k8s/01-configmap.yaml
	k3s kubectl apply -f k8s/02-secrets.yaml
	k3s kubectl apply -f k8s/03-persistent-volumes.yaml
	k3s kubectl apply -f k8s/04-postgres.yaml
	k3s kubectl apply -f k8s/05-rabbitmq.yaml
	k3s kubectl apply -f k8s/06-grafana.yaml
	k3s kubectl apply -f k8s/07-worker.yaml
	k3s kubectl apply -f k8s/08-ingress.yaml
	k3s kubectl apply -f k8s/09-cgpstar.yaml
	k3s kubectl apply -f k8s/10-dev-container.yaml

# K8S COMMANDS:
# *****************************************************************************
k_install_new:
	@zsh k8s/install_microk8s.sh;

k_cgp_builds:
	@sudo DOCKER_BUILDKIT=1 docker build -f docker/Dockerfile_start_again --target=cgp-nt-again -t cgp-nt-again .

k_cgp_images:
	@sudo sh k8s/k8s_images_push.sh;

k_reset_cgp:
	@sudo microk8s kubectl delete -f k8s/07-worker.yaml
	@sudo microk8s kubectl apply -f k8s/07-worker.yaml

k_reset_star:
	@sudo microk8s kubectl delete -f k8s/09-cgpstar.yaml
	@sudo microk8s kubectl apply -f k8s/09-cgpstar.yaml

k_reset_dev:
	@sudo microk8s kubectl delete -f k8s/10-dev-container.yaml
	@sudo microk8s kubectl apply -f k8s/10-dev-container.yaml

k_apply_2:
	@sudo sh k8s/k8s_apply_2.sh;

k_apply:
	@sudo sh k8s/k8s_apply.sh;

k_delete:
	@sudo sh k8s/k8s_delete.sh;

k_pdash:
	@microk8s dashboard-proxy --token-ttl=43200

k_f_graf:
	@microk8s kubectl port-forward service/cgp-grafana 3000:3000  -n cgp-system --request-timeout='0'
k_f_rmq1:
	@microk8s kubectl port-forward service/cgp-rabbitmq 15672:15672  -n cgp-system --request-timeout='0'
k_f_rmq2:
	@microk8s kubectl port-forward service/cgp-rabbitmq 5672:5672  -n cgp-system --request-timeout='0'
k_f_db:
	@microk8s kubectl port-forward service/cgp-database 5432:5432 -n cgp-system --request-timeout='0'

k_st:
	@sudo sh k8s/reg_k8s_start.sh;

k_sp:
	@sudo microk8s stop;

# *****************************************************************************


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

install:
	@poetry install

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
