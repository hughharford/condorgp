import os
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, func
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy.orm import declarative_base, relationship

import sys
sys.path.append('..')

Base = declarative_base()


# NOTE:
# THESE ARE TO CLARIFY THE VARIOUS LAYERS OF DEFINITION:
# Schema classes are singular, and CamelCase. E.g. Individual
# Models classes are plural, and CamelCase. E.g. Individuals
# table names etc are plural and lowercase. E.g. individuals

## REF: https://kitt.lewagon.com/camps/1769/challenges?path=02-Database-Fundamentals%2F04-Backend-and-Database-Management%2F01-Twitter-CRUD

class Comms(Base):
    """Class to represent the comms table"""

    # Table name
    __tablename__ = os.environ.get("COMMS_TABLE", "comms")

    # Columns
    id = Column(Integer, primary_key=True)
    time_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    node = Column(String, nullable=False)
    message = Column(String, nullable=False)
    action = Column(String, nullable=False)

# Individuals (equiv to tweet)
class Individuals(Base):
    """Class to represent the individuals table"""
    # Table name
    __tablename__ = os.environ.get("INDIVIDUALS_TABLE", "individuals")
    # Columns
    ind_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    time_date_logged = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    time_fit_run_start = Column(DateTime(timezone=True))
    fit_run = Column(Boolean, nullable=False)
    fitness = Column(Float, nullable=False)
    ind_string = Column(TEXT, nullable=False) # TEXT psql type is very long indeed
    pop_id = Column(UUID(as_uuid=True), ForeignKey("populations.pop_id"), nullable=False)
    # Relationships
    # NOPE: population = relationship("populations", foreign_keys='individuals.pop_id')
    population = relationship("Populations", back_populates="individual")


# Populations (equiv to like)
class Populations(Base):
    """Class to represent the populations table"""
    # Table name
    __tablename__ = os.environ.get("POPULATIONS_TABLE", "populations")
    # Columns
    pop_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    pop_name = Column(String, nullable=False)
    pop_start_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    num_gens = Column(Integer, nullable=False)
    pop_size = Column(Integer, nullable=False)
    # Relationships
    # NOPE individual = relationship("individuals", foreign_keys='populations.pop_id')
    individual = relationship("Individuals", back_populates="population")




# class Checkpoints(Base):
#     """Class to represent the checkpoints table"""

#     # Table name
#     __tablename__ = os.environ.get("CHECKPOINTS_TABLE", "checkpoints")

#     # Columns
#     checkpoint_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
#     checkpoint_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     checkpoint_path = Column(String, nullable=False)
