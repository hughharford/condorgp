#!/usr/bin/env python

# from:
# https://www.rabbitmq.com/tutorials/tutorial-one-python

import pika

import os

key = 'PIKA_URL_MANUAL'
PIKA_URL = os.getenv(key)

def send():
    connection = pika.BlockingConnection(pika.ConnectionParameters(PIKA_URL))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body='Hello World!')
    print(" [x] Sent 'Hello World!'")


if __name__ == "__main__":
    send()
