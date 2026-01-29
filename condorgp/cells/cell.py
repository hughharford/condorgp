from random import *
import logging

import random, time_uuid


class Cell:
    # Cell types, shared across all objects in the class


    # CONSTANT class data types
    CELL_TYPES = ("PROTOTYPE", "ALIVE", "DEAD")
    CELL_STATUS = ("PERCENTAGE", "CONSTANT", "BELOW_THRESHOLD")
    CELL_SCORE_STATUS = ("TO SCORE", "SCORED")

    def __init__(self
                 , new_cell_ref=888
                 , new_cell_type="PROTOTYPE"
                 , score=0
                 , status="BELOW_THRESHOLD"
                 , score_status="TO SCORE"):

        '''
        input parameters:
            new_cell_ref: identifying integer (888 is default)
            new_cell_type: one of "PROTOTYPE", "ALIVE", "DEAD"
        '''

        self.score_hist = []
        self.cell_ref = new_cell_ref
        # check type is valid
        if (not new_cell_type in Cell.CELL_TYPES):
            raise ValueError(f'{new_cell_type} is not a valid cell type')
        else:
            rand_time = lambda: float(random.randrange(0,30))+time_uuid.utctime()
            t_uuid = time_uuid.TimeUUID.with_timestamp(rand_time())
            self.t_uuid = t_uuid
            self.cell_type = new_cell_type
            self.score = score
            self.status = status
            self.score_status = "TO SCORE"


def main():
    # access the class type:
    print("Cell types: ", Cell.CELL_TYPES)

    cell_central = Cell()

    # # declare cells
    c_one = Cell(new_cell_ref="1089", new_cell_type="PROTOTYPE")
    c_two = Cell(new_cell_ref="0808", new_cell_type="FOR ANALYSIS")

    print(c_one.__dict__)


if __name__ == '__main__':
    main()
