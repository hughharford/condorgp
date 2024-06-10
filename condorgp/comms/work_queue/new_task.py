#!/usr/bin/env python

# from:
# https://www.rabbitmq.com/tutorials/tutorial-two-python

import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)
print(f" [x] Sent {message}")
