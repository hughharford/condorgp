# ----------------------------------
#          INSTALL
# ----------------------------------

install:
	@make maybe_update_env
	@make install_requirements
	@make new_install
	@sh scripts/establish_logs_n_checkpoints.sh
	@make k3d_bootstrap

install_requirements:
	@if command -v poetry >/dev/null 2>&1; then \
		echo "poetry already installed"; \
	elif command -v pipx >/dev/null 2>&1; then \
		pipx install poetry==1.8.4; \
	else \
		python3 -m pip install --user poetry==1.8.4; \
	fi
	@poetry install

new_install:
	@echo checking paths
	@sh scripts/dependencies/checking_env.sh

update_env:
	@direnv allow

maybe_update_env:
	@if command -v direnv >/dev/null 2>&1 && [ -f .envrc ]; then \
		direnv allow; \
	else \
		echo "direnv/.envrc not available, skipping direnv allow"; \
	fi

k3d_check:
	@bash scripts/dependencies/check_k3d_deps.sh

k3d_bootstrap:
	@bash scripts/dependencies/install_k3d_deps.sh
	@make k3d_check

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
	@sudo systemctl restart docker

gefyra_loop_start:
	@sh k8s/k3d/gefyra_setup.sh

gefyra_loop_apply:
	@sh k8s/k3d/apply_gefyra.sh

gefyra_loop_stop:
	@KUBECONFIG=$(HOME)/.kube/gefyra-kubeconfig.yaml gefyra down

gefyra_run_worker:
	@KUBECONFIG=$(HOME)/.kube/gefyra-kubeconfig.yaml gefyra run -d -N worker -n cgp-system --connection-name cgp-system -i k3d-cgp-registry.localhost:30123/cgp-nt-again -c "sleep infinity"

gefyra_bridge_worker:
	@KUBECONFIG=$(HOME)/.kube/gefyra-kubeconfig.yaml gefyra bridge -N worker --connection-name cgp-system -n cgp-system --target deployment/cgp-worker-1/worker -p 2727:2727

gefyra_dev_worker:
	@bash k8s/k3d/gefyra_dev_worker.sh

gefyra_dev_shell:
	@bash k8s/k3d/gefyra_dev_worker.sh

gefyra_dev_worker_run:
	@DETACH=0 DEV_CMD="python condorgp/cgp_rabbitmq/delegate/run_delegated_evals_4_w_strat.py" bash k8s/k3d/gefyra_dev_worker.sh

gefyra_dev_local_http:
	@DETACH=0 DEV_CMD="python k8s/k3d/gefyra/local.py 2727" bash k8s/k3d/gefyra_dev_worker.sh


k3d_out_config:
	@k3d kubeconfig get cgp-cluster > k8s/k3d/output-kube-config.yaml
	@export KUBECONFIG="$(k3d kubeconfig get cgpcluster-)"


k3d_full_reset:
	@sh k8s/k3d/w_reg_n_api_reg_start_k3d.sh
	@sh k8s/k3d/images_push_k3d.sh
	@sh k8s/k3d/apply_k3d.sh
	@make k3d_dash

k3d_del:
	@sh k8s/k3d/cluster_delete_k3d.sh

k3d_stop:
	@k3d cluster stop cgp-cluster

k3d_apply:
	@sh k8s/k3d/apply_k3d.sh

k3d_dash:
	@sh k8s/k3d/dash_kubeconfig.sh

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

test_k3d:
	@PYTHONPATH=. poetry run pytest tests/step_defs/test_015_k3d_start_steps.py -q

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
