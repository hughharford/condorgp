from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
import os

Base = declarative_base()


class Comms(Base):
    """Class to represent the comms table"""

    # Table name
    # __tablename__ =
    __tablename__ = os.environ.get("COMMS_TABLE", "comms")

    # Columns
    id = Column(Integer, primary_key=True)
    node = Column(String, nullable=False)
    message = Column(String, nullable=False)
    action = Column(String, nullable=False)
