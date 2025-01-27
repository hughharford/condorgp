from sqlalchemy.orm import Session

from cgp_api import models, schemas

####### Comms section #######
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
