#!/usr/bin/env python

# from:
# https://www.rabbitmq.com/tutorials/tutorial-two-python

import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='cgp_queue')

message = ' '.join(sys.argv[1:]) or "Start CondorGP standard run!"
channel.basic_publish(exchange='',
                      routing_key='cgp_queue',
                      body=message)

print(f" [x] Sent {message}")
