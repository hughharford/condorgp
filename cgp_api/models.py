import os
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

## REF: https://kitt.lewagon.com/camps/1769/challenges?path=02-Database-Fundamentals%2F04-Backend-and-Database-Management%2F01-Twitter-CRUD

class Comms(Base):
    """Class to represent the comms table"""

    # Table name
    # __tablename__ =
    __tablename__ = os.environ.get("COMMS_TABLE", "comms")

    # Columns
    id = Column(Integer, primary_key=True)
    time_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    node = Column(String, nullable=False)
    message = Column(String, nullable=False)
    action = Column(String, nullable=False)


class Individuals(Base):
    """Class to represent the individuals table"""

    # Table name
    # __tablename__ =
    __tablename__ = os.environ.get("INDIVIDUALS_TABLE", "individuals")

    # Columns
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    time_date_logged = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    time_fit_run_start = Column(DateTime(timezone=True))
    fit_run = Column(Boolean, nullable=False)
    fitness = Column(Float, nullable=False)
    ind_string = Column(String, nullable=False)
