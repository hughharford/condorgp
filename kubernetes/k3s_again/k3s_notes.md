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
