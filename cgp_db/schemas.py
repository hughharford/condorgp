from pydantic import BaseModel, ConfigDict
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

## REF: https://kitt.lewagon.com/camps/1769/challenges?path=02-Database-Fundamentals%2F04-Backend-and-Database-Management%2F01-Twitter-CRUD

# comms
class CommsBase(BaseModel):
    message: str
class CommsCreate(CommsBase):
    node: str
    action: str

class Comms(CommsBase):
    time_date: datetime
    id: int
    class Config:
        from_attributes = True


# individuals
class IndividualsBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    ind_string: str | None = None

class IndividualsCreate(IndividualsBase):
    time_fit_run_start: datetime | None = None
    fit_run: bool | None = False
    fitness: float | None = -55000

class Individuals(IndividualsBase):
    time_date_logged: datetime # | None = datetime.now(pytz.utc)
    ind_id: UUID # | None = uuid.uuid4()
    class Config:
        from_attributes = True


# populations
class PopulationsBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    pop_name: str | None = None

class PopulationsCreate(PopulationsBase):
    pop_start_time: datetime
    num_gens: int | None = 0
    pop_size: int | None = 0

class Populations(PopulationsBase):
    pop_id: UUID 
    class Config:
        from_attributes = True
