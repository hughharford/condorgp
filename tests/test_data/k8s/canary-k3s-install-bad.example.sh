#!/bin/bash
# CANARY (topic G): a deliberately BAD k3s install command that must stay in
# the repo.
#
# Tests 022 use it to prove the repository-wide mode check can FAIL: it makes
# the admin kubeconfig readable by every user, by flag and by variable.
#
# Every value is FAKE. Do not fix this file. It lives under tests/, which the
# repository scan never reads, so it does not trip the real checks.
curl -sfL https://example.invalid/install | sh -s - --write-kubeconfig-mode 644
K3S_KUBECONFIG_MODE=644 sh install.sh
