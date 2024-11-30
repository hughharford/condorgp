from pydantic import BaseModel

# Comms section


class CommsBase(BaseModel):
    message: str


class CommsCreate(CommsBase):
    node: str
    action: str


class Comms(CommsBase):
    id: int

    class Config:
        orm_mode = True
