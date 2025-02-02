#!/usr/bin/env python


import pika
import sys, os
import logging, time, json

QUEUE_FIT_RETURN = 'cgp_fit_return'

def run_delegated_evaluation():

    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost", 5672, "/", credentials)
        )

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_FIT_RETURN, durable=True)

    def callback(ch, method, properties, body):
        parsed_body = json.loads(body)
        logging.error(f" [x] Received {body.decode()}")
        logging.error(f" fitness {parsed_body['fitness']}")

        # logging.error(f" [x] got a fitness back {body.fitness}")
        logging.error(" DEL_1 running >>>> NAUTILUS__TRADER evaluation >>>")
        print(" DEL_1 running >>>> NAUTILUS__TRADER evaluation >>>")

        logging.error(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count=1) # ensures only 1 per consumer
    channel.basic_consume(queue=QUEUE_FIT_RETURN,
                        on_message_callback=callback)

    logging.error(""">>> READY:
                  Waiting for fitness messages.
                  To exit press CTRL+C """)
    channel.start_consuming()


def main():
    run_delegated_evaluation()

if __name__ == '__main__':
    try:
        time.sleep(10)
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
