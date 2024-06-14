#!/usr/bin/env python

# from:
# https://www.rabbitmq.com/tutorials/tutorial-two-python

import pika, sys, os

# read rabbitmq connection url from environment variable
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

# connect to rabbitmq
connection = pika.BlockingConnection(url_params)

# to connect to docker, but only from local
credentials = pika.PlainCredentials("guest", "guest")
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters("localhost", 5672, "/", credentials)
#     )

# for localhost service
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    
channel = connection.channel()

channel.queue_declare(queue='cgp_queue')

message = ' '.join(sys.argv[1:]) or "Start CondorGP standard run!"
channel.basic_publish(exchange='',
                      routing_key='cgp_queue',
                      body=message)

print(f" [x] Sent {message}")
