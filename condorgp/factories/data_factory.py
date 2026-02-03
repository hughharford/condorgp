import logging
from condorgp.data_wranglers.nautilus_raw import NautilusRaw

class DataFactory():
    def __init__(self):
        pass

    def nautilus_raw(self):
        logging.debug(f"DataFactory getting data objects")
        return NautilusRaw()
