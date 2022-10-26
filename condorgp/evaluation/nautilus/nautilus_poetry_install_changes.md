# imports don't work initally...

    ## e.g.
        from nautilus_trader.examples.indicators import ema_py
        # /home/hsth/code/hughharford/nautilus/nautilus_trader/examples/indicators/ema_py.py
        OR
        from nautilus_trader.backtest.data.providers import TestDataProvider
      both should work...
      this shows the relative path, which vs code picks up, but then fails
      # from .....nautilus_trader.persistence.catalog import ParquetDataCatalog

# TO SORT THIS:
  # in vs code 'Python' screen:
      # find the Pyenv..nautilus python verison / environment and set to default


# THIS LOT WOULD WORK, but you need the know the above...
    # looking at:
        # https://stackoverflow.com/questions/71229685/packages-installed-with-poetry-fail-to-import
        # links to:
        # https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment

      # this didn't help....
