# CANARY (topic E): a deliberately BAD Makefile target that must stay in the
# repo. Tests 020 use it to prove the Makefile check can FAIL: it opens the
# retired dashboard, with no short-lived token and no headlamp port-forward.
# Every value is FAKE. Do not fix this file.
k_dash:
	microk8s dashboard-proxy
