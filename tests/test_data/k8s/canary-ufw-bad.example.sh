#!/bin/bash
# CANARY (topic F): a deliberately BAD firewall script that must stay in the
# repo.
#
# Tests 021 use it to prove the firewall checks can FAIL. It does everything
# the real script must never do: it opens SSH and the API to the whole
# internet, opens the unencrypted Flannel VXLAN port, never allows outgoing
# traffic, enables the firewall before allowing SSH, accepts any input, touches
# the firewall even in a dry run, and applies rules other than the ones it
# prints.
#
# Every value is FAKE. Do not fix this file. It lives under tests/, which the
# repository scan never reads, so it does not trip the real checks.
printf '%s\n' \
  "ufw --force enable" \
  "ufw allow from any to any port 22 proto tcp" \
  "ufw default deny incoming" \
  "ufw allow from 0.0.0.0/0 to any port 6443 proto tcp" \
  "ufw allow from 198.51.100.9 to any port 8472 proto udp"
# It calls the program named by CANARY_UFW, which the tests point at a
# recording fake. Without it this is a harmless `true`, so running the canary
# can never touch a real firewall.
"${CANARY_UFW:-true}" allow 22/tcp
