

import pika, sys, os


def get_rmq_connection():

    rmq_username = os.environ('RMQ_USER')
    rmq_password = os.environ('RMQ_PASSWORD')

    credentials = pika.PlainCredentials(rmq_username, rmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost", 5672, "/", credentials)
        )
    return connection
