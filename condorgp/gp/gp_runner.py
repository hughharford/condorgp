import time
import logging
import traceback
import math
import random

from condorgp.params import Params #, util_dict, test_dict, lean_dict
from condorgp.factories.factory import Factory

from condorgp.gp.gp_control import GpControl

if __name__ == "__main__":
    gpc = GpControl()
    gpc.undertake_run()
