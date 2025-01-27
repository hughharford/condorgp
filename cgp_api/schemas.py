from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

## REF: https://kitt.lewagon.com/camps/1769/challenges?path=02-Database-Fundamentals%2F04-Backend-and-Database-Management%2F01-Twitter-CRUD

# Comms section
class CommsBase(BaseModel):
    message: str
class CommsCreate(CommsBase):
    node: str
    action: str

class Comms(CommsBase):
    time_date: datetime
    id: int
    class Config:
        orm_mode = True


# individuals section
class IndividualBase(BaseModel):
    ind_string: str

class IndividualCreate(IndividualBase):
    time_fit_run_start: datetime
    fit_run: bool
    fitness: float

class Individual(IndividualBase):
    time_date_logged: datetime
    id: UUID
    class Config:
        orm_mode = True
