#!/usr/bin/env python

import time
import pika, sys, os
from cgp_rabbitmq import get_rabbitmq_connection

QUEUE_DELEG_EVALS = 'cgp_delegated_eval'

def send_delegate_eval(message):

    connection = get_rabbitmq_connection.get_rmq_connection()
    # credentials = pika.PlainCredentials("guest", "guest")
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters("localhost", 5672, "/", credentials)
    #     )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_DELEG_EVALS, durable=True)

    message = message or (' '.join(sys.argv[1:])) or "Start CondorGP Nautilus evaluation run!"
    channel.basic_publish(exchange='',
                        routing_key=QUEUE_DELEG_EVALS,
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode=pika.DeliveryMode.Persistent
                        ))
    print(f" [x] Sent {message}")


def main():
    for i in range(10):
        sample_message = f"I'm only a delegated evaluation sample {i}"
        send_delegate_eval(sample_message)
        time.sleep(60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
