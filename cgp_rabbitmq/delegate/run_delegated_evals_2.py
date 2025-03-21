#!/usr/bin/env python

# from:
# https://www.rabbitmq.com/tutorials/tutorial-two-python

import pika
from condorgp.gp.gp_control import GpControl
import sys, os
import logging, time
from cgp_rabbitmq.delegate import delegate_eval
from cgp_rabbitmq import get_rabbitmq_connection

QUEUE_DELEG_EVALS =  delegate_eval.QUEUE_DELEG_EVALS

def run_delegated_evaluation():

    connection = get_rabbitmq_connection.get_rmq_connection()

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_DELEG_EVALS, durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        print(" [x] attempting task")
        print(" DEL_2 running >>>> NAUTILUS__TRADER evaluation >>>")
        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)


    channel.basic_qos(prefetch_count=1) # ensures only 1 per consumer
    channel.basic_consume(queue=QUEUE_DELEG_EVALS,
                        on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def main():
    run_delegated_evaluation()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
