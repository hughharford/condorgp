
from decimal import Decimal

import pandas as pd

from nautilus_trader.common.enums import LogColor
from nautilus_trader.config import StrategyConfig
# from nautilus_trader.core.correctness import PyCondition
# from nautilus_trader.core.data import Data
# from nautilus_trader.core.message import Event
# from nautilus_trader.indicators.average.ema import ExponentialMovingAverage
# from nautilus_trader.model.data import Bar
# from nautilus_trader.model.data import BarType
# from nautilus_trader.model.data import OrderBookDeltas
# from nautilus_trader.model.data import QuoteTick
# from nautilus_trader.model.data import Ticker
# from nautilus_trader.model.data import TradeTick
# from nautilus_trader.model.enums import OrderSide
# from nautilus_trader.model.identifiers import InstrumentId
# from nautilus_trader.model.instruments import Instrument
# # from nautilus_trader.model.orderbook import OrderBook
# from nautilus_trader.model.orders import MarketOrder
# from nautilus_trader.trading.strategy import Strategy

from condorgp.evaluation.gp_run_strat_base import GpRunStrategyBaseConfig
from condorgp.evaluation.gp_run_strat_base import GpRunStrategyBase

from condorgp.params import Params

import logging

# *** THIS IS A TEST STRATEGY WITH NO ALPHA ADVANTAGE WHATSOEVER. ***
# *** IT IS NOT INTENDED TO BE USED TO TRADE LIVE WITH REAL MONEY. ***

# was ema_cross.py - directly taken from Nautilus trader
# then adapted


class GpStratInject01(GpRunStrategyBase):
    """
    First injection of gp evolved strategies

    """

    def __init__(self, config: GpRunStrategyBaseConfig, ev_strategy=None) -> None:

        super().__init__(config)

        if ev_strategy:
            self.ev_strategy = ev_strategy

        self.p = Params()
        self.verbosity = self.p.naut_dict['VERBOSITY']

    def __main__(self):
        return self

    def check_triggers(self, blank = ""):

            if self.verbosity: # note, this will log for every bar checked
                logging.debug(
                    f"GpRunStrategyInject.check_triggers: {self.ev_strategy}")

            # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            # THE BELOW IS DIRECTLY FROM EMACROSS
            # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''

            self.log.info("<< WORKING EVOLUTION INJECTION >>", LogColor.YELLOW)

            # BUY LOGIC
            if self.fast_ema.value >= self.slow_ema.value:
                if self.portfolio.is_flat(self.instrument_id):
                    self.buy()
                elif self.portfolio.is_net_short(self.instrument_id):
                    self.close_all_positions(self.instrument_id)
                    self.buy()


            # SELL LOGIC
            elif self.fast_ema.value < self.slow_ema.value:
                if self.portfolio.is_flat(self.instrument_id):
                    self.sell()
                elif self.portfolio.is_net_long(self.instrument_id):
                    self.close_all_positions(self.instrument_id)
                    self.sell()
