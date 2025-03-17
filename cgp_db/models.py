import os
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, func
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy.orm import declarative_base, relationship

# is this really a good idea?
# from cgp_db.schemas import Populations, Individuals, Comms
import sys
sys.path.append('..')

Base = declarative_base()

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

    population = relationship("populations", foreign_keys='individuals.pop_id')


# sample only - to delete
# class Friend(Base):
#     __tablename__ = 'friend'

#     user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
#     user = relationship('User', foreign_keys='Friend.user_id')

#     friend_id = Column(Integer, ForeignKey(User.id), primary_key=True)
#     friend = relationship('User', foreign_keys='Friend.friend_id')

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

    individual = relationship("individuals", foreign_keys='populations.pop_id')




# class Checkpoints(Base):
#     """Class to represent the checkpoints table"""

#     # Table name
#     __tablename__ = os.environ.get("CHECKPOINTS_TABLE", "checkpoints")

#     # Columns
#     checkpoint_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
#     checkpoint_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     checkpoint_path = Column(String, nullable=False)
