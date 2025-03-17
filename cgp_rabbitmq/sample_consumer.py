import pika
import uuid
import pytz
from datetime import datetime
import os
from cgp_db.database import SessionLocal
from cgp_db import models, schemas
from sqlalchemy.dialects.postgresql import UUID

from cgp_rabbitmq import get_rabbitmq_connection

def get_db():
    """Helper function which opens a connection to the
    database and also manages closing the connection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def callback(ch, method, properties, body):

    with SessionLocal() as db:

        data = body.decode('utf-8').split(":")
        print(data)
        print(f"Received individual {data[2]} with fitness: {data[5]}")

        db_pops = schemas.PopulationsCreate()
        db_pops.pop_name = "trial"
        db_pops.pop_size = 10
        db_pops.num_gens = 2
        db_pops.pop_start_time = datetime.now(pytz.utc)

        print(db_pops.__dict__)
        db_ingoing = models.Populations(**db_pops.model_dump())

        newpopid = uuid.uuid4()
        db_ingoing.pop_id = newpopid

        db.add(db_ingoing)
        db.commit()
        db.refresh(db_ingoing)


        db_inds = schemas.IndividualsCreate()
        db_inds.fit_run = bool(data[4])
        db_inds.time_fit_run_start = datetime.now(pytz.utc)
        db_inds.fitness = float(data[5])
        db_inds.ind_string = str(data[6])

        # foreign key population_id = populations.pop_id

        db_ingoing = models.Individuals(**db_inds.model_dump())
        db_ingoing.pop_id = uuid.uuid4() # newpopid
        db_ingoing.ind_id = uuid.uuid4()
        db.add(db_ingoing)
        db.commit()
        db.refresh(db_ingoing)

def main():

    connection = get_rabbitmq_connection.get_rmq_connection()

    channel = connection.channel()
    queue='individuals'
    channel.queue_declare(queue=queue)

    channel.basic_consume(queue='individuals', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
