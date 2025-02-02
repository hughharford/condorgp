from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from cgp_db import crud, schemas
from cgp_db.database import SessionLocal

tags = [
    {"name": "CGP Backbone ", "description": "Recorder of CGP"},
]

app = FastAPI(title="CGP Backbone Database", openapi_tags=tags)


def get_db():
    """Helper function which opens a connection to the
    database and also manages closing the connection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# App landing page
@app.get("/")
def read_root():
    return {"CGP webapi": "Running"}


####### Comms section #######
@app.post("/comms/", response_model=schemas.Comms, tags=["comms"])
def create_comms_for_node(comms: schemas.CommsCreate, db: Session = Depends(get_db)):
    """post endpoint to create a new comms for a given node id"""
    return crud.create_comms(db=db, comms=comms)


@app.get("/get_comms/", response_model=List[schemas.Comms], tags=["comms"])
def read_comms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """get endpoint to read all the the comms"""
    comms = crud.read_comms(db, skip=skip, limit=limit)
    return comms
