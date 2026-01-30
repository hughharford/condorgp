#!/usr/bin/env python


import pika
import sys, os
import logging, time
from cgp_rabbitmq import get_rabbitmq_connection

QUEUE_DELEG_EVALS = 'cgp_delegated_eval'

def run_delegated_evaluation():


    connection = get_rabbitmq_connection.get_rmq_connection()
    # credentials = pika.PlainCredentials("guest", "guest")
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters("localhost", 5672, "/", credentials)
    #     )

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_DELEG_EVALS, durable=True)

    def callback(ch, method, properties, body):
        logging.error(f" [x] Received {body.decode()}")
        logging.error(" [x] attempting task")
        logging.error(" DEL_1 running >>>> NAUTILUS__TRADER evaluation >>>")
        print(" DEL_1 running >>>> NAUTILUS__TRADER evaluation >>>")

        logging.error(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count=1) # ensures only 1 per consumer
    channel.basic_consume(queue=QUEUE_DELEG_EVALS,
                        on_message_callback=callback)

    logging.error(">>> READY: [*] Waiting for messages. To exit press CTRL+C ")
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def main():
    run_delegated_evaluation()

if __name__ == '__main__':
    try:
        # time.sleep(10)
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
