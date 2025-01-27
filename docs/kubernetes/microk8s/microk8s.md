# followed these instructions:
## https://microk8s.io/


# MASTER SETUP


sudo snap install microk8s --classic

microk8s status --wait-ready

microk8s enable dashboard

>> enabled user to microk8s group




microk8s dashboard-proxy


# ADD NODE
## https://microk8s.io/docs/clustering

### on master:
  microk8s add-node
  > get worker node join line, with --worker

do this on master:
sudo ufw allow 1338
sudo ufw allow 2380
sudo ufw allow 12379
sudo ufw allow 16443
sudo ufw allow 19001
sudo ufw allow 25000
sudo ufw allow 10248
sudo ufw allow 10249
sudo ufw allow 10250
sudo ufw allow 10251
sudo ufw allow 10252
sudo ufw allow 10253
sudo ufw allow 10254
sudo ufw allow 10255
sudo ufw allow 10256
sudo ufw allow 10257
sudo ufw allow 10258
sudo ufw allow 10259

sudo ufw status

this covers all the ports listed:
https://microk8s.io/docs/ports

### on node:
sudo snap install microk8s --classic

microk8s join 192.168.1.100:25000/<token> --worker
