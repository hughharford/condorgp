# K3S again

## getting moving. start stop etc

make k3_stop
sudo systemctl stop k3s
make k3_start
sudo systemctl start k3s

## REFS

https://docs.k3s.io/upgrades/killall

## full reset with KILL ALL

bash /usr/local/bin/k3s-killall.sh
-- this worked!

### Get status

systemctl status k3s
-- this works

## k3s agent .kubeconfig

/var/lib/rancher/k3s/agent/kubelet.kubeconfig

## k3s paths

/var/lib/rancher/k3s/agent/
/var/lib/rancher/k3s/data/
/var/lib/rancher/k3s/server/

## symlink? files together

REF:
https://www.freecodecamp.org/news/symlink-tutorial-in-linux-how-to-create-and-remove-a-symbolic-link/

e.g.
ln -s /var/lib/rancher/k3s/agent/kubelet.kubeconfig
 /home/hsth/code/hughharford/condorgp/kubernetes/k3s_again/simlinked_files/kubelet_s.kubeconfig
