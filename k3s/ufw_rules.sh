#!/usr/bin/env bash
# ufw_rules.sh - firewall rules for a hub-and-spoke k3s cluster running over the internet.
#
# Every inbound rule names a source address. Nothing is opened to "anywhere".
# By default this only PRINTS the rules (a dry run). Add APPLY=1 to run them.
#
#   HUB (the k3s server):
#     sudo ROLE=hub   ADMIN_IP=<your.public.ip> NODE_IPS="<spoke1> <spoke2>" APPLY=1 bash k3s/ufw_rules.sh
#   SPOKE (a k3s agent):
#     sudo ROLE=spoke ADMIN_IP=<your.public.ip> NODE_IPS="<hub> <other spokes>" APPLY=1 bash k3s/ufw_rules.sh
#
#   ADMIN_IP   the address (or small CIDR, /16 or narrower) you administer from. Required.
#              It is the ONLY source allowed to SSH in, so a wrong value locks you out.
#   NODE_IPS   the other cluster machines' public IPs, space or comma separated. Required.
#   SSH_PORT   default 22
#   POD_NET_RULES=0   leave out the two k3s pod/service network rules (default 1)
#
# Ports (https://docs.k3s.io/installation/requirements#inbound-rules-for-k3s-nodes):
#   22/tcp     SSH                         from ADMIN_IP only
#   6443/tcp   Kubernetes API              hub only: from ADMIN_IP and every node
#   51820/udp  WireGuard (flannel, IPv4)   from every node
#   51821/udp  WireGuard (flannel, IPv6)   from every node
#   10250/tcp  kubelet                     from every node
# 8472/udp (flannel VXLAN) is never opened: it is not encrypted. The cluster uses
# flannel-backend wireguard-native instead. See kubernetes/k3s_again/k3s_hub_spoke.md.
#
# IPv4 only. The default-deny policy also applies to IPv6 if ufw's IPV6=yes.
# Order matters: SSH is allowed BEFORE default-deny and enable, so you are not locked out.
# If you ever add a rule by hand, always include "from <address>".

set -euo pipefail

ROLE="${ROLE:-}"
ADMIN_IP="${ADMIN_IP:-}"
NODE_IPS="${NODE_IPS:-}"
SSH_PORT="${SSH_PORT:-22}"
POD_NET_RULES="${POD_NET_RULES:-1}"
APPLY="${APPLY:-0}"

die() { echo "ERROR: $*" >&2; exit 1; }

# valid_source <value> <min-prefix>: dotted IPv4, optionally /N with N >= min-prefix. Never 0.0.0.0.
valid_source() {
  local v="$1" min="$2" ip prefix octet
  [[ "$v" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}(/[0-9]{1,2})?$ ]] || return 1
  ip="${v%%/*}"
  prefix=32
  [[ "$v" == */* ]] && prefix="${v##*/}"
  IFS=. read -ra octets <<<"$ip"
  for octet in "${octets[@]}"; do (( 10#$octet <= 255 )) || return 1; done
  [ "$ip" != "0.0.0.0" ] || return 1
  (( 10#$prefix >= min && 10#$prefix <= 32 )) || return 1
}

case "$ROLE" in hub|spoke) ;; *) die "ROLE must be 'hub' or 'spoke' (got '${ROLE}')" ;; esac
[ -n "$ADMIN_IP" ] || die "ADMIN_IP is required (the only address allowed to SSH in)"
valid_source "$ADMIN_IP" 16 || die "ADMIN_IP '$ADMIN_IP' is not a specific IPv4 address or a /16-or-narrower range"
[[ "$SSH_PORT" =~ ^[0-9]{1,5}$ ]] && (( SSH_PORT >= 1 && SSH_PORT <= 65535 )) || die "SSH_PORT '$SSH_PORT' is not a port number"
[[ "$POD_NET_RULES" =~ ^[01]$ ]] || die "POD_NET_RULES must be 0 or 1"
[[ "$APPLY" =~ ^[01]$ ]] || die "APPLY must be 0 or 1"

nodes=()
for n in ${NODE_IPS//,/ }; do
  valid_source "$n" 24 || die "NODE_IPS entry '$n' is not a specific IPv4 address or a /24-or-narrower range"
  nodes+=("$n")
done
[ "${#nodes[@]}" -gt 0 ] || die "NODE_IPS is required (the other cluster machines' public IPs)"

rules=()
add() { rules+=("$*"); }

# 1. SSH from the admin first, so nothing after it can lock the admin out.
add "ufw allow from $ADMIN_IP to any port $SSH_PORT proto tcp"
# 2. API: the hub accepts it from the admin and from every node. Spokes never host it.
if [ "$ROLE" = hub ]; then
  add "ufw allow from $ADMIN_IP to any port 6443 proto tcp"
  for n in "${nodes[@]}"; do add "ufw allow from $n to any port 6443 proto tcp"; done
fi
# 3. Node-to-node: WireGuard overlay + kubelet.
for n in "${nodes[@]}"; do
  add "ufw allow from $n to any port 51820 proto udp"
  add "ufw allow from $n to any port 51821 proto udp"
  add "ufw allow from $n to any port 10250 proto tcp"
done
# 4. k3s' own pod and service networks (k3s docs: needed so pods can reach the host).
if [ "$POD_NET_RULES" = 1 ]; then
  add "ufw allow from 10.42.0.0/16 to any"
  add "ufw allow from 10.43.0.0/16 to any"
fi
# 5. Policy last.
add "ufw default deny incoming"
add "ufw default allow outgoing"
add "ufw --force enable"

printf '%s\n' "${rules[@]}"

if [ "$APPLY" = 1 ]; then
  for r in "${rules[@]}"; do
    # shellcheck disable=SC2086  # rules contain no spaces inside a word, by construction
    ${r}
  done
  echo "# applied ${#rules[@]} rules. Check with: sudo ufw status numbered" >&2
else
  echo "# DRY RUN: nothing was changed. Re-run with APPLY=1 (as root) to apply." >&2
fi
