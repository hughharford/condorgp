import logging


class Cell:
    # Cell types, shared across all objects in the class
    '''
        basic cell establishment and operations, for CondorGP

        the idea here is exceptionally basic.
        essentially:
            1. cells are created, and a list kept of them
            2. they can only have certain states

        future needs, in no particular order:
            A. Visualise the cells, their sizes, activity rate etc
            B. Be able to show the visualisation somewhere easy, e.g. Streamlit share public

    '''

    # CONSTANT class data types
    CELL_TYPES = ("PROTOTYPE", "ALIVE", "DEAD", "FOR ANALYSIS")
    CELL_STATUS = ("PERCENTAGE", "CONSTANT", "BELOW_THRESHOLD")


    # class property to hold list of dicts about the Cells
    __cells = None

    def __init__(self, new_cell_ref=888, new_cell_type="PROTOTYPE"):
        '''
        input parameters:
            new_cell_ref: identifying integer (888 is default)
            new_cell_type: one of "PROTOTYPE", "ALIVE", "DEAD", "FOR ANALYSIS"
        '''
        self.cell_ref = new_cell_ref

        # check type is valid
        if (not new_cell_type in Cell.CELL_TYPES):
            raise ValueError(f'{new_cell_type} is not a valid cell type')
        else:
            self.cell_type = new_cell_type

        # once defined, add to master list
        Cell.add_cell_to_cell_set(self.cell_ref, self.cell_type)


    @classmethod
    def get_cell_list(cls):
        '''static method to retrieve single list of Cells'''
        if Cell.__cells == None:
            Cell.__cells = set()
        return Cell.__cells

    # TODO: witness function

    @classmethod
    def add_cell_to_cell_set(cls, newref, newtype):
        '''static method to single cell to list of Cells'''
        Cell.get_cell_list()
        Cell.__cells.add((newref, newtype))

    @staticmethod
    def show_cell_list():
        # see the cells
        if (not Cell.__cells):
            raise AttributeError('no cells found')
        else:
            for c in Cell.__cells:
                print(f'Cell: {c}')

    @staticmethod
    def get_cell_count():
        # see the cells
        if (not Cell.__cells):
            raise AttributeError('no cells found')
        else:
            return len(Cell.__cells)

    @classmethod
    def get_cell_types(cls):
        '''class method to return class type, e.g. CELL_TYPES'''
        return Cell.CELL_TYPES

    @classmethod
    def get_cell_types(cls):
        '''class method to return class type, e.g. CELL_TYPES'''
        return Cell.CELL_TYPES

    def set_cell_ref(self, new_ref):
        '''instance method that sets the cell reference id'''
        self.cell_ref = new_ref

    @staticmethod
    def cell_death(cell_ref=None):
        if cell_ref:
            logging.debug(f'cell.cell_death {cell_ref} removal.')
            Cell.remove_cell(cell_ref)
        else:
            logging.error(f'cell.cell_death cell_ref == None.')
            return 0

    @staticmethod
    def check_if_cell_ref_exists(cell_ref):
        '''static method to confirm if cell is extant, by cell_ref'''
        for c in Cell.__cells:
            print(c['cell_ref'])
            if cell_ref == c['cell_ref']: return 1
            else: return 0

    @classmethod
    def remove_cell(cls, cell_ref_to_remove=()):
        '''static method to remove a single cell'''
        if cell_ref_to_remove:
            print(f'removing cell with  ref no: {cell_ref_to_remove}')
            Cell.__cells.discard(cell_ref_to_remove)
            print(f'ACTION: to specific cell {cell_ref_to_remove} removed')

def main():
    # access the class type:
    print("Cell types: ", Cell.get_cell_types())

    # declare cells
    c1 = Cell(new_cell_ref="001", new_cell_type="PROTOTYPE")
    c2 = Cell(new_cell_ref="002", new_cell_type="PROTOTYPE")
    print(Cell.get_cell_count())
    c3 = Cell(new_cell_ref="003", new_cell_type="ALIVE")
    c4 = Cell(new_cell_ref="004", new_cell_type="DEAD")
    c5 = Cell(new_cell_ref="005", new_cell_type="FOR ANALYSIS")
    print(Cell.get_cell_count())

    cell_list = Cell.get_cell_list()

    Cell.show_cell_list()

    Cell.remove_cell()
    print(Cell.get_cell_count())

    Cell.remove_cell(('001','PROTOTYPE'))
    print(Cell.get_cell_count())
    Cell.show_cell_list()

    # Cell.cell_death("002")
    # print(Cell.get_cell_count())


if __name__ == '__main__':
    main()
