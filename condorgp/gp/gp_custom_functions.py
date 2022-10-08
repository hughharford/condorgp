import numpy
from condorgp.params import test_dict
from condorgp.factories.initial_factory import InitialFactory



class GpCustomFunctions:
    ''' keep custom functions in here. '''
    def __init__(self):
        pass

        # Define new functions
    def protectedDiv(left, right):
        with numpy.errstate(divide='ignore',invalid='ignore'):
            x = numpy.divide(left, right)
            if isinstance(x, numpy.ndarray):
                x[numpy.isinf(x)] = 1
                x[numpy.isnan(x)] = 1
            elif numpy.isinf(x) or numpy.isnan(x):
                x = 1
        return x

    def test_C_func(x0):
        pass
