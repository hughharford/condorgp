# copied from Nautilus site:
# https://docs.nautilustrader.io/getting_started/quick_start.html
# but data ingestion altered to follow:
# https://docs.nautilustrader.io/user_guide/loading_external_data.html


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
from nautilus_trader.persistence.external.readers import TextReader

# addition
from nautilus_trader.examples.strategies import ema_cross

#/home/hsth/code/hughharford/nautilus/condorgp/data
DATA_DIR = "/home/hsth/code/hughharford/nautilus/condorgp/data/"
#  DATA_DIR = "data/"

fs = fsspec.filesystem('file')
raw_files = fs.glob(f"{DATA_DIR}/naut_fx/HISTDATA*")
assert raw_files, f"Unable to find any histdata files in directory {DATA_DIR}"
if raw_files:
    print('using these files: ')
    for f in raw_files:
        print(f)


import datetime
import pandas as pd
from nautilus_trader.model.data.tick import QuoteTick
from nautilus_trader.model.objects import Price, Quantity
from nautilus_trader.core.datetime import dt_to_unix_nanos

def parser(data, instrument_id):
    """ Parser function for hist_data FX data, for use with CSV Reader """
    dt = pd.Timestamp(datetime.datetime.strptime(data['timestamp'].decode(), "%Y%m%d %H%M%S%f"), tz='UTC')
    yield QuoteTick(
        instrument_id=instrument_id,
        bid=Price.from_str(data['bid'].decode()),
        ask=Price.from_str(data['ask'].decode()),
        bid_size=Quantity.from_int(100_000),
        ask_size=Quantity.from_int(100_000),
        ts_event=dt_to_unix_nanos(dt),
        ts_init=dt_to_unix_nanos(dt),
    )

CATALOG_PATH = DATA_DIR + "/naut_catalog/"

# Clear if it already exists, then create fresh
if os.path.exists(CATALOG_PATH):
    shutil.rmtree(CATALOG_PATH)
os.mkdir(CATALOG_PATH)

catalog = ParquetDataCatalog(CATALOG_PATH)

print(catalog)

from nautilus_trader.persistence.external.core import process_files, write_objects
from nautilus_trader.backtest.data.providers import TestInstrumentProvider

# Use nautilus test helpers to create a EUR/USD FX instrument for our purposes
instrument = TestInstrumentProvider.default_fx_ccy("EUR/GBP")

from nautilus_trader.persistence.external.core import write_objects

write_objects(catalog, [instrument])

print(catalog.instruments())

from nautilus_trader.persistence.external.core import process_files
from nautilus_trader.persistence.external.readers import CSVReader


process_files(
    glob_path=raw_files,
    reader=CSVReader(
        block_parser=lambda x: parser(x, instrument_id=instrument.id),
        header=['timestamp', 'bid', 'ask', 'volume'],
        chunked=False,
        as_dataframe=False,
    ),
    catalog=catalog,
)

if catalog.list_data_types():
    print('catalog.instruments() is POPULATED \n')
    print(catalog.list_data_types())
else:
    print('catalog.instruments() is STILL empty \n')

#  print(catalog.instruments())
start = dt_to_unix_nanos(pd.Timestamp('2008-01-01', tz='UTC'))
end =  dt_to_unix_nanos(pd.Timestamp('2008-01-30', tz='UTC'))


venues_config=[
    BacktestVenueConfig(
        name="SIM",
        oms_type="HEDGING",
        account_type="MARGIN",
        base_currency="GBP",
        starting_balances=["1000000 GBP"],
    )
]

data_config=[
    BacktestDataConfig(
        catalog_path=CATALOG_PATH,
        data_cls=QuoteTick,
        instrument_id=instrument.id.value,
        start_time=start,
        end_time=end,
    )
]

strategies = [
    ImportableStrategyConfig(
        strategy_path="nautilus_trader.examples.strategies.ema_cross:EMACross",
        config_path="nautilus_trader.examples.strategies.ema_cross:EMACrossConfig",
        config=ema_cross.EMACrossConfig(
            instrument_id=instrument.id.value,
            bar_type="EUR/GBP.SIM-15-MINUTE-BID-INTERNAL",
            fast_ema=10,
            slow_ema=20,
            trade_size=Decimal(1_000_000),
        ),
    ),
]

config = BacktestRunConfig(
    engine=BacktestEngineConfig(strategies=strategies),
    data=data_config,
    venues=venues_config,
)

node = BacktestNode(configs=[config])

results = node.run()
