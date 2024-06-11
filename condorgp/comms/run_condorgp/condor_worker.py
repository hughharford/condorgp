#!/usr/bin/env python

# from:
# https://www.rabbitmq.com/tutorials/tutorial-two-python

import pika
from condorgp.gp.gp_control import GpControl
import sys, os
import logging, time

def main():
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='cgp_queue')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        # time.sleep(body.count(b'.'))
        print(" [x] attempting task")
        
        gpc = GpControl()
        gpc.undertake_run()
        
        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)
        
    channel.basic_consume(queue='cgp_queue',
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
