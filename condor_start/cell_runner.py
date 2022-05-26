

class Cell:
    # Cell types, shared across all objects in the class
    '''
        basic cell establishment and operations, for CondorGP
    '''

    CELL_TYPES = ("PROTOTYPE", "ALIVE", "DEAD", "FOR ANALYSIS")
    CELL_STATUS = ("PERCENTAGE", "CONSTANT", "BELOW_THRESHOLD")


    # class property to hold list of Cells
    __celllist = None

    def __init__(self, newref=888, newcelltype="PROTOTYPE"):
        self.cellref = newref
        if (not newcelltype in Cell.CELL_TYPES):
            raise ValueError(f'{newcelltype} is not a valid cell type')
        else:
            self.celltype = newcelltype

        # record new cell in Class list of cells
        internalcelllist = Cell.getcelllist()

        if (not internalcelllist == None):
            internalcelllist.append(self)
        else:
            print("internal __celllist not working")

    # static method to retrieve single list of Cells
    @staticmethod
    def getcelllist():
        if Cell.__celllist == None:
            Cell.__celllist = []
        return Cell.__celllist
    # TODO: witness function

    @staticmethod
    def showcelllist():
        # see the cells
        if (not Cell.__celllist):
            raise AttributeError('no cells found')
        else:
            for c in Cell.__celllist:
                print('Cell ref:', c.cellref, c)


    # class method to return class type, e.g. CELL_TYPES
    @classmethod
    def getcelltypes(cls):
        return Cell.CELL_TYPES

    # instance methods
    def setcellref(self, newref):
        self.cellref = newref


def main():
    # access the class type:
    print("Cell types: ", Cell.getcelltypes())

    # declare cells
    c1 = Cell("001", "PROTOTYPE")
    c2 = Cell("002", "PROTOTYPE")

    Cell.showcelllist()



if __name__ == '__main__': main()
