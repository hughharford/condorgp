#!/usr/bin/env python

# from:
# https://www.rabbitmq.com/tutorials/tutorial-two-python

import pika, sys, os

QUEUE_DELEG_EVALS = 'cgp_delegated_eval'

def send_delegate_eval(message):

    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost", 5672, "/", credentials)
        )
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
    sample_message = "I'm only a delegated evaluation sample"
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
