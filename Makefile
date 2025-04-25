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
