#!/usr/bin/env python

import pika, sys, os
import random
import json

from cgp_rabbitmq import get_rabbitmq_connection

QUEUE_FIT_RETURN = 'cgp_fit_return'

def send_delegate_eval(message):

    connection = get_rabbitmq_connection.get_rmq_connection()

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_FIT_RETURN, durable=True)

    message = message or (' '.join(sys.argv[1:])) or "Return fitnesses from Nautilus Evaluation!"
    channel.basic_publish(exchange='',
                        routing_key=QUEUE_FIT_RETURN,
                        body=json.dumps(message),
                        properties=pika.BasicProperties(
                            delivery_mode=pika.DeliveryMode.Persistent
                        ))
    print(f" [x] Sent {message}")


def main():
    fitness = random.uniform(10.0,100.0)
    message = "sample text"
    sample_message = {"message": message, "fitness": fitness}
    send_delegate_eval(sample_message)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
