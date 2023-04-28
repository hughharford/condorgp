# copied from Nautilus site:
# https://docs.nautilustrader.io/getting_started/quick_start.html

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

EUR_GBP = TestInstrumentProvider.default_fx_ccy("EUR/GBP")

def parser(line):
    ts, bid, ask, idx = line.split(b",")
    dt = pd.Timestamp(datetime.datetime.strptime(ts.decode(), "%Y%m%d %H%M%S%f"), tz='UTC')
    yield QuoteTick(
        instrument_id=EUR_GBP.id,
        bid=Price.from_str(bid.decode()),
        ask=Price.from_str(ask.decode()),
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

def run_process_files():
    process_files(
        glob_path=f"{DATA_DIR}/HISTDATA*.zip",
        reader=TextReader(line_parser=parser),
        catalog=catalog,
    )
    write_objects(catalog, [EUR_GBP])

run_process_files()

print(catalog)

# Also manually write the EUR v GBP fx instrument to the catalog


start = dt_to_unix_nanos(pd.Timestamp('2008-01-01', tz='UTC'))
end =  dt_to_unix_nanos(pd.Timestamp('2008-01-30', tz='UTC'))

# catalog.quote_ticks(start=start, end=end)

# catalog.quote_ticks(catalog.instruments())
# catalog.quote_ticks(instruments=catalog.instruments(), start=start, end=end, path=CATALOG_PATH)
# catalog.quote_ticks(['currency_pair'], start=start, end=end)
# catalog.quote_ticks(EUR_GBP, start=start, end=end)

# qt = catalog.quote_ticks(['EUR_GBP'])
# print(qt)
instruments = catalog.instruments(as_nautilus=True)

if catalog.list_data_types():
    print('catalog.instruments() is POPULATED \n', catalog.list_data_types())
else:
    print('catalog.instruments() is STILL empty \n')

# print(catalog.__dict__, '\n\n')
# print('list_data_types: ', catalog.list_data_types())


venues_config=[
    BacktestVenueConfig(
        name="SIM",
        oms_type="HEDGING",
        account_type="MARGIN",
        base_currency="USD",
        starting_balances=["1000000 USD"],
    )
]

data_config=[
    BacktestDataConfig(
        catalog_path=CATALOG_PATH,
        data_cls=instruments[0], # QuoteTick, # NOPE< DIDN@T WORK
        instrument_id = str(instruments[0].id), # instrument_id=instrument.id.value,
        start_time=start,
        end_time=end,
    )
]

strategies = [
    ImportableStrategyConfig(
        strategy_path="nautilus_trader.examples.strategies.ema_cross:EMACross",
        config_path="nautilus_trader.examples.strategies.ema_cross:EMACrossConfig",
        config=ema_cross.EMACrossConfig(
            instrument_id=instruments[0].id.value, # =instrument.id.value,
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
