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


    # class property to hold list of Cells
    __cell_list = None

    def __init__(self, newref=888, new_cell_type="PROTOTYPE"):
        '''
        input parameters:
            ref_id: identifying integer
            cell_type: one of "PROTOTYPE", "ALIVE", "DEAD", "FOR ANALYSIS"
        '''
        self.cell_ref = newref

        # check type is valid
        if (not new_cell_type in Cell.CELL_TYPES):
            raise ValueError(f'{new_cell_type} is not a valid cell type')
        else:
            self.celltype = new_cell_type

        # once defined, add to master list
        Cell.add_cell_to_cell_list(self)


    @staticmethod
    def get_cell_list():
        '''static method to retrieve single list of Cells'''
        if Cell.__cell_list == None:
            Cell.__cell_list = []
        return Cell.__cell_list

    # TODO: witness function

    @staticmethod
    def add_cell_to_cell_list(cell):
        '''static method to single cell to list of Cells'''
        lst = Cell.get_cell_list()
        lst.append(cell)

    @staticmethod
    def check_if_cell_ref_exists(cell_ref):
        for c in Cell.__cell_list:
            if cell_ref == c.cell_ref: return 1
            else: return 0

    @staticmethod
    def remove_cell(cell_ref_to_remove=''):
        '''static method to remove a single cell'''
        if cell_ref_to_remove:
            print('removing cell with  ref no: ' + cell_ref_to_remove)
            Cell.__cell_list.remove(cell_ref_to_remove)
            if cell_ref_to_remove in Cell.__cell_list:
                Cell.__cell_list.remove(cell_ref_to_remove)
            print(f'ACTION: to specific cell {cell_ref_to_remove} removed!')
        else:
            # assume the first cell [0]
            cell_list = Cell.get_cell_list()
            cell_for_removal = cell_list[-1]
            print('cell_for_removal: ' + cell_for_removal.cell_ref)
            cell_list.pop()
            print('if there was no error, the last cell has been popped')

    @staticmethod
    def show_cell_list():
        # see the cells
        if (not Cell.__cell_list):
            raise AttributeError('no cells found')
        else:
            for c in Cell.__cell_list:
                print('Cell ref:', c.cell_ref, c)

    @staticmethod
    def get_cell_count():
        # see the cells
        if (not Cell.__cell_list):
            raise AttributeError('no cells found')
        else:
            return len(Cell.__cell_list)

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


def main():
    # access the class type:
    print("Cell types: ", Cell.get_cell_types())

    # declare cells
    c1 = Cell("001", "PROTOTYPE")
    c2 = Cell("002", "PROTOTYPE")
    c3 = Cell("003", "PROTOTYPE")


    cell_list = Cell.get_cell_list()
    for c in cell_list:
        Cell.check_if_cell_ref_exists(c.cell_ref)

    Cell.show_cell_list()
    print(Cell.get_cell_count())

    Cell.remove_cell()
    print(Cell.get_cell_count())

    Cell.remove_cell("001")
    print(Cell.get_cell_count())

    Cell.cell_death("002")
    print(Cell.get_cell_count())


if __name__ == '__main__':
    main()
