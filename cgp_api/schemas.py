from pydantic import BaseModel, ConfigDict
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
class IndividualsBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    ind_string: str | None = None

class IndividualsCreate(IndividualsBase):
    time_fit_run_start: datetime | None = None
    fit_run: bool | None = False
    fitness: float | None = -55000

class Individuals(IndividualsBase):
    time_date_logged: datetime # | None = datetime.now(pytz.utc)
    id: UUID # | None = uuid.uuid4()
    class Config:
        orm_mode = True
