import pika
import uuid
import pytz
from datetime import datetime
from cgp_api.database import SessionLocal
from cgp_api import models, schemas
from sqlalchemy.dialects.postgresql import UUID


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
        # print(
        #     db.execute(
        #         """
        #     SELECT * FROM information_schema.tables
        #     WHERE table_schema = 'public'
        #     """
        #     ).fetchall()
        # )

        # db.execute('USE cgp_backbone')


        data = body.decode('utf-8').split(":")
        print(data)
        print(f"Received individual {data[2]} with fitness: {data[5]}")

        db_inds = schemas.IndividualsCreate()
        db_inds.fit_run = bool(data[4])
        db_inds.time_fit_run_start = datetime.now(pytz.utc)
        db_inds.fitness = float(data[5])
        db_inds.ind_string = str(data[6])

        db_ingoing = models.Individuals(**db_inds.model_dump())
        db_ingoing.id = uuid.uuid4()
        db.add(db_ingoing)
        db.commit()
        db.refresh(db_ingoing)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    queue='individuals'
    channel.queue_declare(queue=queue)

    channel.basic_consume(queue='individuals', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
