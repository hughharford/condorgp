#!/usr/bin/env python

# from:
# https://www.rabbitmq.com/tutorials/tutorial-one-python

import pika
import os, sys

key = 'PIKA_URL_MANUAL'
PIKA_URL = os.getenv(key)


def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters(PIKA_URL))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='hello',
                        auto_ack=True,
                        on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
