# rabbitmqctl install:
?

# installing rabbitmq:
https://www.rabbitmq.com/docs/download
https://www.rabbitmq.com/docs/install-debian
### see: 
cloudsmith_quick_start_script.sh

# run local rabbitmq:
# latest RabbitMQ 3.13 on DOCKER
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management


# CONTROLLING LOCAL NODE
##### CANNOT RUN DOCKER AND LOCALHOST SERVICE TOGETHER
##### DOCKER BETTER
# stop the local node
sudo systemctl stop rabbitmq-server
# start it back
sudo systemctl start rabbitmq-server

# check rabbitmq server: (only for localhost, not docker)
sudo rabbitmqctl status 

### at the bottom:
Listeners

Interface: [::], port: 25672, protocol: clustering, purpose: inter-node and CLI tool communication
Interface: [::], port: 5672, protocol: amqp, purpose: AMQP 0-9-1 and AMQP 1.0


# Stop rabbitmq service:
sudo rabbitmqctl stop
### or
sudo rabbitmqctl stop_app 


# to see RabbitMQ management console in the browser:
http://localhost:15672/#/
password and username: guest



### response when trying to start rabbitmq '3' docker
initially:
  Error starting userland proxy: listen tcp4 0.0.0.0:25672: bind: address already in use.
then once sudo rabbitmqctl stop ran:
  Error starting userland proxy: listen tcp4 0.0.0.0:4369: bind: address already in use.

  ### trying:
  https://serverfault.com/questions/283913/turn-off-epmd-listening-port-4369-in-ubuntu-rabbitmq
  #### useful but not relevant



# Management command line tool: 
# rabbitmqadmin
https://www.rabbitmq.com/docs/management-cli
### install via:
https://stackoverflow.com/questions/36336071/install-rabbitmqadmin-on-linux
but chmod 755 not 777
### also?
chmod +x 
### list queues:
rabbitmqadmin -f tsv -q list queues
### delete queues:
rabbitmqadmin delete queue name=name_of_queue
### add binding between exchange and queue
rabbitmqadmin declare binding source="exchangename" destination_type="queue" destination="queuename" routing_key="routingkey"

### suggested better:
sudo rabbitmq-plugins enable rabbitmq_management
wget 'https://raw.githubusercontent.com/rabbitmq/rabbitmq-management/v3.7.15/bin/rabbitmqadmin'
chmod +x rabbitmqadmin
sed -i 's|#!/usr/bin/env python|#!/usr/bin/env python3|' rabbitmqadmin
mv rabbitmqadmin .local/bin/
rabbitmqadmin -q list queues
