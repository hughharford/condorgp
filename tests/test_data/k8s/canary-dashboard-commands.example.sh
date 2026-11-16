#!/bin/bash
# CANARY (topic E): deliberately BAD dashboard commands that must stay in the
# repo.
#
# Tests 020 use this file to prove the script checks can FAIL: it installs the
# retired Kubernetes Dashboard, creates a cluster-admin binding and exposes a
# port-forward to every network interface.
#
# Every value is FAKE. Do not fix this file. It lives under tests/, which the
# repository scan never reads, so it does not trip the real checks.
kubectl apply -f https://example.invalid/kubernetes/dashboard/v2.7.0/recommended.yaml
kubectl create clusterrolebinding canary-admin --clusterrole=cluster-admin --serviceaccount=canary-ui:dashboard-admin
kubectl -n canary-ui port-forward service/canary-dash 8443:443 --address 0.0.0.0
