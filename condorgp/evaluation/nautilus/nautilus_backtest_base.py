# copied from Nautilus site:
# https://docs.nautilustrader.io/getting_started/quick_start.html
# but data ingestion altered to follow:
# https://docs.nautilustrader.io/user_guide/loading_external_data.html
##
# adapted into a class for inital use in CondorGP



import datetime
import os
import shutil
from decimal import Decimal

import fsspec
import pandas as pd
from nautilus_trader.core.datetime import dt_to_unix_nanos
from nautilus_trader.model.data.tick import QuoteTick
from nautilus_trader.model.objects import Price, Quantity

from nautilus_trader.backtest.data.providers import TestInstrumentProvider
from nautilus_trader.backtest.node import BacktestNode, BacktestVenueConfig, BacktestDataConfig, BacktestRunConfig, BacktestEngineConfig
from nautilus_trader.config.common import ImportableStrategyConfig
from nautilus_trader.persistence.catalog import ParquetDataCatalog
from nautilus_trader.persistence.external.core import process_files, write_objects
from nautilus_trader.persistence.external.readers import CSVReader
# addition
from nautilus_trader.examples.strategies import ema_cross



class NautilusBacktestBase():
    '''
    A framework to start for Nautilus use for now
    If this goes well, lots more to follow.

    '''

    def __init__(self):
        ''' most basic start'''
        #/home/hsth/code/hughharford/nautilus/condorgp/data
        self.DATA_DIR = "/home/hsth/code/hughharford/nautilus/condorgp/data/"
        self.CATALOG_PATH = self.DATA_DIR + "/naut_catalog/"

    def setup_files(self):
        ''' Setup filesystem and ensure >1 available '''
        self.fs = fsspec.filesystem('file')
        self.raw_files = self.fs.glob(f"{self.DATA_DIR}/naut_fx/HISTDATA*")
        assert self.raw_files, f"Unable to find any histdata files in directory {self.DATA_DIR}"
        if self.raw_files:
            print('using these files: ')
            for f in self.raw_files:
                print(f)

    def parser(self, data, instrument_id):
        """ Parser function for hist_data FX data, for use with CSV Reader """
        dt = pd.Timestamp(
            datetime.datetime.strptime(
                data['timestamp'].decode(),
                "%Y%m%d %H%M%S%f"), tz='UTC')
        yield QuoteTick(
            instrument_id=instrument_id,
            bid=Price.from_str(data['bid'].decode()),
            ask=Price.from_str(data['ask'].decode()),
            bid_size=Quantity.from_int(100_000),
            ask_size=Quantity.from_int(100_000),
            ts_event=dt_to_unix_nanos(dt),
            ts_init=dt_to_unix_nanos(dt),
        )

    def set_catalog(self):
        # Clear if it already exists, then create fresh
        if os.path.exists(self.CATALOG_PATH):
            shutil.rmtree(self.CATALOG_PATH)
        os.mkdir(self.CATALOG_PATH)

        self.catalog = ParquetDataCatalog(self.CATALOG_PATH)
        print(self.catalog)

    def set_instruments(self):
        '''create a EUR/USD FX instrument with nautilus test helpers'''
        self.instrument = TestInstrumentProvider.default_fx_ccy("EUR/GBP")
        write_objects(self.catalog, [self.instrument])
        print(self.catalog.instruments())

    def process_input_data(self):
        process_files(
            glob_path=self.raw_files,
            reader=CSVReader(
                block_parser=lambda x: self.parser(
                            x,
                            instrument_id=self.instrument.id
                            ),
                header=['timestamp', 'bid', 'ask', 'volume'],
                chunked=False,
                as_dataframe=False,
            ),
            catalog=self.catalog,
        )

    def set_limits(self):
        #  print(catalog.instruments())
        self.start = dt_to_unix_nanos(pd.Timestamp('2008-01-01', tz='UTC'))
        self.end =  dt_to_unix_nanos(pd.Timestamp('2008-01-30', tz='UTC'))

    def examine_catalog(self):
        if self.catalog.list_data_types():
            print('catalog.instruments() is POPULATED \n')
            print(self.catalog.list_data_types())
        else:
            print('catalog.instruments() is STILL empty \n')

    def configure_backtester(self):
        self.venues_config=[
            BacktestVenueConfig(
                name="SIM",
                oms_type="HEDGING",
                account_type="MARGIN",
                base_currency="GBP",
                starting_balances=["1000000 GBP"],
            )
        ]

        self.data_config=[
            BacktestDataConfig(
                catalog_path=self.CATALOG_PATH,
                data_cls=QuoteTick,
                instrument_id=self.instrument.id.value,
                start_time=self.start,
                end_time=self.end,
            )
        ]

        self.strategies = [
            ImportableStrategyConfig(
                strategy_path="nautilus_trader.examples.strategies.ema_cross:EMACross",
                config_path="nautilus_trader.examples.strategies.ema_cross:EMACrossConfig",
                config=ema_cross.EMACrossConfig(
                    instrument_id=self.instrument.id.value,
                    bar_type="EUR/GBP.SIM-15-MINUTE-BID-INTERNAL",
                    fast_ema=10,
                    slow_ema=20,
                    trade_size=Decimal(1_000_000),
                ),
            ),
        ]

        self.config = BacktestRunConfig(
            engine=BacktestEngineConfig(strategies=self.strategies),
            data=self.data_config,
            venues=self.venues_config,
        )

        self.node = BacktestNode(configs=[self.config])

    def do_run(self):
        self.results = self.node.run()

    def basic_run_through(self):
        self.setup_files()
        self.set_catalog()
        self.set_instruments()
        self.process_input_data()
        self.set_limits()
        self.configure_backtester()
        self.do_run()

if __name__ == "__main__":
    nbt = NautilusBacktestBase()
    nbt.basic_run_through()

        #
