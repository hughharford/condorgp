<!--
CANARY (topic G): a deliberately BAD k3s guide that must stay in the repo.

Tests 022 use it to prove the guide check can FAIL: it tells the reader to make
the kubeconfig world-readable, and never explains how to use a private one.

Every value is FAKE. Do not fix this file. It lives under tests/, which the
repository scan never reads, so it does not trip the real checks.
-->
# FAKE k3s notes

Install the hub with `--write-kubeconfig-mode 644` so that kubectl just works.
