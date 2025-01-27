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

    # db = get_db()

    with SessionLocal() as db:
        print(
            db.execute(
                """
            SELECT * FROM information_schema.tables
            WHERE table_schema = 'public'
            """
            ).fetchall()
        )

        # db.execute('USE cgp_backbone')


        data = body.decode('utf-8').split(":")
        ind_id = str(uuid.uuid4())
        time_date_logged = data[0]
        fit_run = data[1]
        time_fit_run_start = str(datetime.now(pytz.utc))
        fitness = data[2]
        ind_string = data[3]
        print(f"Received individual {ind_id} with fitness: ${fitness}")
        # save = (ind_id, time_date_logged, time_fit_run_start, fit_run, fitness, ind_string)
        # query = f'INSERT INTO individuals VALUES ({ind_id}, "{time_date_logged}", "{time_fit_run_start}", "{fit_run}", "{fitness}", "{ind_string}")'
        # db.execute(query)

        db_inds = models.Individuals(UUID, time_date_logged, time_fit_run_start, fit_run, fitness, ind_string)
        db.add(db_inds)
        db.commit()
        db.refresh(db_inds)

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
