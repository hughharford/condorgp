

import pika, sys, os

def get_rmq_connection():
    rmq_username = os.getenv('RMQ_USER')
    rmq_password = os.getenv('RMQ_PASSWORD')
    RUNNER = os.getenv('WHERE_IS_RABBIT')


    credentials = pika.PlainCredentials(rmq_username, rmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(RUNNER, 5672, "/", credentials)
        )
    return connection

if __name__ == "__main__":
    get_rmq_connection()
