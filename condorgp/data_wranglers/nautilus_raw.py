import logging
from pathlib import Path

from condorgp.params import Params

from nautilus_trader.persistence.catalog import ParquetDataCatalog

class NautilusRaw:
    '''class to prove data wrangling'''
    def __init__(self):
        logging.debug(f"{__name__} initialising...")
        self.data_objs = []
        self.catalogs = []
        self.data_path = Params().naut_dict['NAUT_DATA_PATH']
        self.posix_data_path = Path(self.data_path)
        assert self.posix_data_path

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
        return 0

    def setup_catalog(self, path):
        '''creates catalog from existing data on the given path'''

        CATALOG_PATH = Path.cwd() / "catalog"
        assert CATALOG_PATH
        # Create a new catalog instance
        self.catalog = ParquetDataCatalog(CATALOG_PATH)
        # Should fail, no data on path
        assert type(self.catalog) == ParquetDataCatalog

        self.data_objs = self.catalog.bars()

if __name__ == "__main__":
    nr = NautilusRaw()
    p = Params()
    print(f"on objects: {nr.get_no_objs()}")
    print(f"expectations: {nr.show_expectations()}")
    nr.setup_catalog(p.naut_dict['NAUT_DATA_PATH'])
    print(f"on objects: {nr.get_no_objs()}")
