import numpy
from condorgp.params import test_dict



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

    def get_extant_line(self):
        extant_line = '''
    def newly_injected_code(self):
        return ConstantAlphaModel(InsightType.Price,
                                  InsightDirection.Up,
                                  timedelta(minutes = 20),
                                  0.025, None
                                  )'''
        return extant_line

    def get_alpha_model_A(self, x0):
        line = '''
    def newly_injected_code(self):
        return HistoricalReturnsAlphaModel()'''
        return line

    def get_alpha_model_B(self, x0):
        line = '''
    def newly_injected_code(self):
        return EmaCrossAlphaModel()'''
        return line

    def get_alpha_model_C(self):
        line = '''
    def newly_injected_code(self):
        return MacdAlphaModel()'''
        return line

    def get_alpha_model_D(self):
        line = '''
    def newly_injected_code(self):
        return RsiAlphaModel()'''
        return line
