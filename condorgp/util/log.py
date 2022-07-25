import logging

from condorgp.params import util_dict

class CondorLogger():
    def __init__(self):
        self.log = logging.getLogger(__name__)

        # logging.basicConfig(
        #         format='%(asctime)s - %(levelname)s - %(message)s',
        #         level=logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s -  %(levelname)s - %(message)s')
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                                                    # useless name

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        ch.setFormatter(formatter)

        # set basic file handler
        fh = logging.FileHandler(filename = util_dict['CONDOR_LOG'],
                                 mode='a',
                                 encoding=None,
                                 delay=False,)
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)

        # add handlers to logger
        self.log.addHandler(ch)
        self.log.addHandler(fh)


    def get_logger(self):
        return self.log
