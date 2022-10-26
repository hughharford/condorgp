# copied from Nautilus site:
#

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

DATA_DIR = "condorgp/data/"

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

process_files(
    glob_path=f"{DATA_DIR}/HISTDATA*.zip",
    reader=TextReader(line_parser=parser),
    catalog=catalog,
)

# Also manually write the EUR v GBP fx instrument to the catalog
write_objects(catalog, [EUR_GBP])

catalog.instruments()

import pandas as pd
from nautilus_trader.core.datetime import dt_to_unix_nanos


start = dt_to_unix_nanos(pd.Timestamp('2008-01-01', tz='UTC'))
end =  dt_to_unix_nanos(pd.Timestamp('2008-01-02', tz='UTC'))


# catalog.quote_ticks(catalog.instruments())
catalog.quote_ticks(instruments=catalog.instruments(), start=start, end=end, path=CATALOG_PATH)
