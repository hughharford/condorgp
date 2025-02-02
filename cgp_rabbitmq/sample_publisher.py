import pika
import random
import time
import pytz
from datetime import datetime

def publish_random_individuals():

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    queue='individuals'
    channel.queue_declare(queue=queue)
    try:
        while True:
            time_fit_run_start = datetime.now(pytz.utc)
            fit_run = True
            fitness = round(random.uniform(-100.0, 200.0), 2)
            ind_string = "simplest individual as string"

            message = f"{time_fit_run_start}:{fit_run}:{fitness}:{ind_string}"
            print(message)
            channel.basic_publish(exchange='', routing_key=queue, body=message)
            time.sleep(random.random())
    finally:
        connection.close()

if __name__ == '__main__':
    publish_random_individuals()
