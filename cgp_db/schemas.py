from pydantic import BaseModel, ConfigDict
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import pytz
import uuid


## REF: https://kitt.lewagon.com/camps/1769/challenges?path=02-Database-Fundamentals%2F04-Backend-and-Database-Management%2F01-Twitter-CRUD

# comms
class CommBase(BaseModel):
    message: str
class CommCreate(CommBase):
    node: str
    action: str

class Comm(CommBase):
    time_date: datetime
    id: int
    class Config:
        from_attributes = True


# individuals (equiv to tweet)
class IndividualBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    ind_string: str
    pop_id: uuid.UUID

class IndividualCreate(IndividualBase):
    time_fit_run_start: datetime | None = None
    fit_run: bool | None = False
    fitness: float | None = -55000

class Individual(IndividualBase):
    time_date_logged: datetime
    ind_id: int # UUID

    class Config:
        from_attributes = True


# populations (equiv to like)
class PopulationBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    pop_name: str
    pop_size: int
    num_gens: int

class PopulationCreate(PopulationBase):
    pop_start_time: datetime | None = datetime.now(pytz.utc)

class Population(PopulationBase):
    pop_id: uuid.UUID
    pop_start_time: datetime
    individuals: list["Individual"] = []

    class Config:
        from_attributes = True


# # checkpoints
# class CheckpointsBase(BaseModel):
#     model_config = ConfigDict(arbitrary_types_allowed=True)

#     checkpoint_path: str | None = None

# class CheckpointsCreate(CheckpointsBase):
#     checkpoint_time: datetime
#     ind_string: str | None = None

# class Checkpoints(CheckpointsBase):
#     checkpoint_id: UUID
#     class Config:
#         from_attributes = True
