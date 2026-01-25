
from random import *
import logging


from condorgp.cells.cell import Cell

class Cells:
    # class property to hold list of dicts about the Cells
    '''
        basic cell establishment and operations, for CondorGP

        the idea here is:
            1. cells are created, and a list kept of them
            2. they can only have certain states

        future needs, in no particular order:
            A. Visualise the cells, their sizes, activity rate etc
            B. Be able to show the visualisation somewhere easy

    '''
    __cell_record = []

    def __init__(self):
        pass

    def new_cell(self, user_ref, celltype, score=0, status="BELOW_THRESHOLD"):
        if user_ref and celltype:
            c = Cell(user_ref, celltype, score, status)
            self.append_cell_to_list(c)

    def append_cell_to_list(self, c):
        '''static method to single cell to list of Cells'''
        self.__cell_record.append(c)

    def get_cell_list(self):
        '''static method to retrieve single list of Cells'''
        if self.__cell_record == None:
            self.__cell_record = []
        return self.__cell_record

    def show_cell_list(self):
        ''' see the cells '''
        if (not self.__cell_record):
            raise AttributeError('no cells found')
        else:
            for c in self.__cell_record:
                data = f'Cell: {c.cell_ref}, {c.cell_type}, {c.score}, {c.status}'
                print(data)
                logging.info(data)

    def show_cell_dict_by_ref(self, cell_ref):
        temp_c = self.get_cell_by_ref(cell_ref)
        out = temp_c.__dict__
        # print(out)
        logging.info(out)
        return temp_c.__dict__

    def get_cell_count(self):
        if (not self.__cell_record):
            logging.debug('Cell.get_cell_count: __cells !extant')
            return 0
        else:
            return len(self.__cell_record)

    @classmethod
    def get_cell_types(cls):
        '''class method to return class type, e.g. CELL_TYPES'''
        return Cell.CELL_TYPES

    def check_if_cell_ref_exists(self, cell_ref):
        '''confirms if cell is extant, by cell_ref'''
        for c in self.__cell_record:
            # print(c.cell_ref)
            if cell_ref == c.cell_ref: return 1
        return 0

    def get_cell_by_ref(self, cell_ref):
        for c in self.__cell_record:
            if cell_ref == c.cell_ref:
                return c
        return 0

    def cell_death_by_ref(self, cell_ref=''):
        cc = self.get_cell_by_ref(cell_ref)
        if cc:
            logging.debug(f'cell {cell_ref} for cell_death .')
            self.remove_specific_cell(cc)
        else:
            logging.error(f'cell.cell_death cell_ref == None.')
            return 0

    def remove_specific_cell(self, c):
        '''Static method to remove a single cell
        Takes cell instance as input
        '''
        tempcount = self.get_cell_count()
        if c:
            print(f'removing cell with  ref no: {c.cell_ref}')
            c_index = self.__cell_record.index(c)
            self.pop_cell(c_index)
            print(f'ACTION: to specific cell {c.cell_ref} removed')
        temp2count = self.get_cell_count()
        if tempcount == temp2count:
            return (0, "failed to remove a cell")
        elif tempcount == (temp2count+1):
            return (0, f"removed cell {c.cell_ref}")

    def pop_cell(self, position=-1):
        '''reduces cell count, returning cell'''
        try:
            return self.__cell_record.pop(position)
        except IndexError as e:
            logging.error(f"No more cells in list {e}, returned []")
            return []

    def simple_static_evaluation_score(self):
        print(len(self.__cell_record))
        for c in self.__cell_record:
            r = randint(1, 100)
            c.score = r
            c.score_hist.append(c.score)

def main():
    # access the class type:
    c = Cells()
    print("Cell types: ", c.get_cell_types())

    # # declare cells
    c.new_cell(user_ref="0808", celltype="ALIVE")
    # print(c.get_cell_count())
    c.new_cell(user_ref="1089", celltype="PROTOTYPE")
    # print(c.get_cell_count())

    # print(c.check_if_cell_ref_exists("88"))
    print("printing!", c.show_cell_dict_by_ref("1089"))

    c.simple_static_evaluation_score()

    c.show_cell_list()

    # this = c.get_cell_by_index("1089")
    # print(this)


if __name__ == '__main__':
    main()
