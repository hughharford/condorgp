import pika
import random
import time
import pytz
from datetime import datetime

from cgp_db import models, schemas, crud, database


def interim_fitness_loop():

    db_inds = []
    no = 0
    with database.SessionLocal() as db:
        while no < 20:
            no+=1
            # time_fit_run_start = datetime.now(pytz.utc)
            fit_run = False
            fitness = round(random.uniform(-100.0, 200.0), 2)
            ind_string = "simplest individual as string"

            #               4                           5                   6=ind_string
            message = {"fit_run":fit_run,"fitness":fitness,"ind_instring":ind_string}
            print(message)
            db_inds.append(crud.record_individual_from_rmq(db, message))

    print(db_inds)

if __name__ == '__main__':
    interim_fitness_loop()

                        # db_inds.fit_run = bool(data[4])
                        # if db_inds.fit_run:
                        #     db_inds.fitness = float(data[5])
                        # else:
                        #     db_inds.fitness = -8899.12

                        # db_inds.time_fit_run_start = datetime.now(pytz.utc)
                        # db_inds.ind_string = str(data[6])

    # db_ingoing = models.Individuals(**db_inds.model_dump())
    # db_ingoing.id = uuid.uuid4()
    # db.add(db_ingoing)
    # db.commit()
    # db.refresh(db_ingoing)
