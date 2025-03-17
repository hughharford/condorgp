# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* condorgp/*.py

black:
	@black scripts/* condorgp/*.py

k8s_forwarding:
	@microk8s kubectl port-forward service/cgp-grafana 3000:3000  -n cgp-system --request-timeout='0' &
	@microk8s kubectl port-forward service/cgp-rabbitmq 15672:15672  -n cgp-system --request-timeout='0' &
	@microk8s kubectl port-forward service/cgp-rabbitmq 5672:5672  -n cgp-system --request-timeout='0' &
	@microk8s kubectl  port-forward service/cgp-database 5432:5432 -n cgp-system --request-timeout='0'  &

k8s_images:
	@sh k8s/k8s_images_push.sh

k8s_start:
	@sh k8s/reg_k8s_start.sh

k8s_stop:
	@sudo microk8s stop

k8s_apply:
	@ sh k8s/k8s_apply.sh

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
	@pip install . -U

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
