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
    __cells = set()

    def __init__(self, new_cell_ref=888, new_cell_type="PROTOTYPE") -> None:
        '''
        input parameters:
            new_cell_ref: identifying integer (888 is default)
            new_cell_type: one of "PROTOTYPE", "ALIVE", "DEAD", "FOR ANALYSIS"
        '''
        # check type is valid
        if (not new_cell_type in Cell.CELL_TYPES):
            raise ValueError(f'{new_cell_type} is not a valid cell type')
        else:
            new_cell_type = "PROTOTYPE"
        self.new_cell_ref = new_cell_ref
        self.new_cell_type = new_cell_type

        # once defined, add to master list
        Cell.add_cell_to_cell_set(self.new_cell_type, self.new_cell_ref)


    @classmethod
    def get_cell_list(cls) -> set:
        '''static method to retrieve single list of Cells'''
        if Cell.__cells == None:
            Cell.__cells = {("cell refs", "cell types")} # set
            return Cell.__cells
        return Cell.__cells

    # TODO: witness function

    def add_cell_to_cell_set(self, new_cell_ref: int, new_cell_type: CELL_TYPES) -> str:
        '''static method to single cell to list of Cells'''
        Cell.new_cell = {new_cell_ref, new_cell_type}
        if Cell.__cells is not None:
            Cell.__cells.update(Cell.new_cell)
            return "Cell added without apparent issue"
        else:
            return "ERROR no __cells or issue with .new_cell"


    @staticmethod
    def show_cell_list() -> None:
        # see the cells
        if (not Cell.__cells):
            raise AttributeError('no cells found')
        else:
            for c in Cell.__cells:
                print(f'Cell: {c}')

    @staticmethod
    def get_cell_count() -> int:
        # see the cells
        if (not Cell.__cells):
            return 0
            logging.debug('Cell.get_cell_count: __cells !extant')
        else:
            return len(Cell.__cells)

    @classmethod
    def get_cell_types(cls) -> tuple:
        '''class method to return class type, e.g. CELL_TYPES'''
        return Cell.CELL_TYPES

    def set_cell_ref(self, new_ref) -> None:
        '''instance method that sets the cell reference id'''
        self.cell_ref = new_ref

    @staticmethod
    def cell_death(cell_ref=None) -> int:
        if cell_ref:
            logging.debug(f'cell.cell_death {cell_ref} removal.')
            Cell.remove_cell(cell_ref)
            return 1
        else:
            logging.error(f'cell.cell_death cell_ref == None.')
            return 0

    @staticmethod
    def check_if_cell_ref_exists(cell_ref) -> int:
        '''static method to confirm if cell is extant, by cell_ref'''
        if cell_ref in Cell.__cells: return 1
        else: return 0

    @classmethod
    def remove_cell(cls, cell_ref_to_remove=()) -> tuple:
        '''static method to remove a single cell'''
        tempcount = Cell.get_cell_count()
        if cell_ref_to_remove:
            print(f'removing cell with  ref no: {cell_ref_to_remove}')
            assert Cell.__cells is not None
            Cell.__cells.discard(cell_ref_to_remove)
            print(f'ACTION: to specific cell {cell_ref_to_remove} removed')
        temp2count = Cell.get_cell_count()
        if tempcount == temp2count:
            return (0, "failed to remove a cell")
        elif tempcount == (temp2count+1):
            return (0, f"removed cell {cell_ref_to_remove}")
        return ()

def main() -> None:
    # access the class type:
    print("Cell types: ", Cell.get_cell_types())

    # declare cells
    c1 = Cell(new_cell_ref=1001, new_cell_type="PROTOTYPE")
    c2 = Cell(new_cell_ref=1002, new_cell_type="PROTOTYPE")
    print(Cell.get_cell_count())
    c3 = Cell(new_cell_ref=1003, new_cell_type="ALIVE")
    c4 = Cell(new_cell_ref=1004, new_cell_type="DEAD")
    c5 = Cell(new_cell_ref=1005, new_cell_type="FOR ANALYSIS")
    print(Cell.get_cell_count())

    cell_list = Cell.get_cell_list()

    Cell.show_cell_list()

    result = Cell.remove_cell()
    print(f'{Cell.get_cell_count()} + {result}')

    result = Cell.remove_cell(('001','PROTOTYPE'))
    print(f'{Cell.get_cell_count()} + {result}')
    Cell.show_cell_list()

    Cell.remove_cell(('004','PROTOTYPE'))
    print(f'{Cell.get_cell_count()} + {result}')
    Cell.show_cell_list()

    Cell.remove_cell(('004','DEAD'))
    print(f'{Cell.get_cell_count()} + {result}')
    Cell.show_cell_list()



if __name__ == '__main__':
    main()
