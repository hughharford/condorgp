import logging
import sys
from condorgp.params import util_dict


loggers = {}

class CondorLogger:
    '''
        home grown logging, see examples below
    '''
    #   # filler_WARN = '&'*15
        # log.warning(f"{filler_WARN}: deap_with_lean, a WARNING message: {__name__}")
        # filler_CRITICAL = '££'*15
        # log.critical(f"{filler_CRITICAL}: deap_with_lean, a WARNING message: {__name__}")
        # log.debug(f"{filler_DEBUG},  DEBUG message: {__name__} - DEAP gp - run began {filler_INIT}")
        # log.info(f"{filler_DEBUG}, INFO message: {__name__} - DEAP gp - run began {filler_INIT}")
        # log.warning(f"{filler_DEBUG}, WARNING message: {__name__} - DEAP gp - run began {filler_INIT}")
        # log.error(f"{filler_DEBUG}, ERROR message: {__name__} - DEAP gp - run began {filler_INIT}")
        # log.critical(f"{filler_DEBUG}, CRITICAL message: {__name__} - DEAP gp - run began {filler_INIT}")


    def __init__(self):

        self.log = logging.getLogger(__name__)
        if (self.log.hasHandlers()):
            self.log.handlers.clear()

        self.log.level=logging.DEBUG # set overall level for logger

        formatter = logging.Formatter('%(asctime)s -  %(levelname)s - %(message)s')

        # further log levels for different handlers - so far to match:
        matching_level = logging.DEBUG # higher (less info): INFO

        # create console handler and set level
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        ch.setLevel(level=matching_level)

        # set basic file handler
        fh = logging.FileHandler(filename = util_dict['CONDOR_LOG'],
                                mode='a',
                                encoding=None,
                                delay=False,
                                )
        fh.setFormatter(formatter)
        fh.setLevel(level=matching_level)

        # add handlers to logger
        self.log.addHandler(ch)
        self.log.addHandler(fh)


    def get_logger(self):
        return self.log
