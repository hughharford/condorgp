
from nautilus_trader.persistence.catalog import ParquetDataCatalog

## all these work / reach their module:
# from nautilus_trader.examples.strategies import ema_cross
# from nautilus_trader.indicators import amat
# from nautilus_trader.indicators.average import ama
# from nautilus_trader.backtest.data.providers import TestDataProvider

catalog = ParquetDataCatalog("./")
catalog.instruments()

if catalog.list_data_types():
    print('catalog.instruments() is POPULATED \n')
else:
    print('catalog.instruments() is STILL empty \n')

# print(catalog.__dict__, '\n\n')
# print('backtests: ', catalog.list_backtests())
# print('list_data_types: ', catalog.list_data_types())
