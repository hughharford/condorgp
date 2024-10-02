import logging
from pathlib import Path

from condorgp.params import Params

from nautilus_trader.persistence.catalog import ParquetDataCatalog

class NautilusRaw:
    '''class to prove data wrangling'''
    def __init__(self):
        self.data_objs = []
        self.catalogs = []
        self.data_path = Params().naut_dict['NAUT_DATA_PATH']
        self.posix_data_path = Path(self.data_path)
        assert self.posix_data_path

        # cgp_data_objs.get_no_objs
    def get_no_objs(self):
        '''returns number of wrangled objects in data_objs[]'''
        return len(self.data_objs)

    def get_default_bar(self):
        '''provides the default bar data'''
        return "default bar (holding position)"

    def get_default_catalog(self):
        '''provides the default catalog'''
        deltas = "nautilus delta"
        self.catalog.write_data(deltas)

    def default_wrangle(self):
        '''wrangles the default data, as per __init__'''
        return 99

    def show_expectations(self):
        '''logs the data wrangling setup, for clarity'''

    def setup_catalog(self, path):
        '''creates catalog from existing data on the given path'''

        CATALOG_PATH = Path.cwd() / "catalog"

        # Create a new catalog instance
        self.catalog = ParquetDataCatalog(CATALOG_PATH)
        # THIS GOTTA FAIL, THERE IS NO DATA THERE
