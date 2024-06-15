#!/usr/bin/env python

# from:
# https://www.rabbitmq.com/tutorials/tutorial-two-python

import pika
from condorgp.gp.gp_control import GpControl
import sys, os
import logging, time

# for use in docker to docker connections

def main():
    queue='cgp_queue'
    
    # to connect to docker, but only from local
    credentials = pika.PlainCredentials("guest", "guest")

    # read rabbitmq connection url from environment variable
    amqp_url = os.environ['AMQP_URL']
    url_params = pika.URLParameters(amqp_url)

    # connect to rabbitmq
    connection = pika.BlockingConnection(url_params)
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        logging.info(f"{'&&&'*3} cgp_w_d: q={queue} [x] Start Task")

        gpc = GpControl()
        gpc.undertake_run()
        
        logging.info(f"{'&&&'*3} cgp_w_d: q={queue} [x] DONE")

        ch.basic_ack(delivery_tag = method.delivery_tag)
        
    channel.basic_consume(queue=queue,
                        on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    logging.info(f"{'&&&'*3} GpControl>cgp_cmd_d: q=cgp_queue [x] Sent {message}")

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
