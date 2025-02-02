from sqlalchemy.orm import Session

from cgp_db import models, schemas
import datetime
import uuid
import pytz


####### Comms section #######
# for api only..
def read_comms(db: Session, skip: int = 0, limit: int = 100):
    """Function should return all comms with a skip and limit param"""
    return db.query(models.Comms).offset(skip).limit(limit).all()

def create_comms(db: Session, comms: schemas.CommsCreate):
    """Function should create a new communication in the database"""
    db_comms = models.Comms(**comms.model_dump())
    db.add(db_comms)
    db.commit()
    db.refresh(db_comms)
    return db_comms


###### Individuals section ######
# for api only..

# def read_comms(db: Session, skip: int = 0, limit: int = 100):
#     """Function should return all individuals with a skip and limit param"""
#     return db.query(models.Individuals).offset(skip).limit(limit).all()

# def create_individuals(db: Session, individuals: schemas.IndividualCreate):
#     """Function should create a new individual in the database"""
#     db_inds = models.Individuals(**individuals.model_dump())
#     db.add(db_inds)
#     db.commit()
#     db.refresh(db_inds)
#     return db_inds


def record_individual(db: Session, message_body):
    '''
    Records individual before fitness check in cgp_backbone db
    In table "individuals"
    '''



    data = message_body.values
    print(data)
    print(f"Received individual {data[2]} with fitness: {data[5]}")

    db_inds = schemas.IndividualsCreate()

    db_inds.fit_run = bool(data[4])
    if db_inds.fit_run:
        db_inds.fitness = float(data[5])
    else:
        db_inds.fitness = -8899.12

    db_inds.time_fit_run_start = datetime.now(pytz.utc)
    db_inds.ind_string = str(data[6])

    db_ingoing = models.Individuals(**db_inds.model_dump())
    db_ingoing.id = uuid.uuid4()
    db.add(db_ingoing)
    db.commit()
    db.refresh(db_ingoing)

    return db_ingoing.id
