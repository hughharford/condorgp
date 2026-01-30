#!/usr/bin/env python

# from:
# https://www.rabbitmq.com/tutorials/tutorial-two-python

import pika, sys, os
import logging

queue='cgp_queue2'

# to connect to docker, but only from local
credentials = pika.PlainCredentials("guest", "guest")

# read rabbitmq connection url from environment variable
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)
# connect to rabbitmq
connection = pika.BlockingConnection(url_params)
channel = connection.channel()
channel.queue_declare(queue=queue, durable=True)

message = ' '.join(sys.argv[1:]) or "Start CondorGP run!"
channel.basic_publish(exchange='',
                      routing_key=queue,
                      body=message)

print(f" [x] Sent {message}")
logging.info(f"{'&&&'*3} GpControl>cgp_cmd_d: q={queue} [x] Sent {message}")
logging.info(f"{'&&&'*3} GpControl>cgp_cmd_d: url={amqp_url}")



