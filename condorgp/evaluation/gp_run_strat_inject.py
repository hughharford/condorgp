# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2023 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

from decimal import Decimal

import pandas as pd

from nautilus_trader.common.enums import LogColor
from nautilus_trader.config import StrategyConfig
from nautilus_trader.core.correctness import PyCondition
from nautilus_trader.core.data import Data
from nautilus_trader.core.message import Event
from nautilus_trader.indicators.average.ema import ExponentialMovingAverage
from nautilus_trader.model.data import Bar
from nautilus_trader.model.data import BarType
from nautilus_trader.model.data import OrderBookDeltas
from nautilus_trader.model.data import QuoteTick
from nautilus_trader.model.data import Ticker
from nautilus_trader.model.data import TradeTick
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.model.orderbook import OrderBook
from nautilus_trader.model.orders import MarketOrder
from nautilus_trader.trading.strategy import Strategy

from condorgp.evaluation.gp_run_strat_base import GpRunStrategyBaseConfig
from condorgp.evaluation.gp_run_strat_base import GpRunStrategyBase

from condorgp.params import Params

import logging

# *** THIS IS A TEST STRATEGY WITH NO ALPHA ADVANTAGE WHATSOEVER. ***
# *** IT IS NOT INTENDED TO BE USED TO TRADE LIVE WITH REAL MONEY. ***

# was ema_cross.py - directly taken from Nautilus trader
# then adapted


class GpRunStrategyInject(GpRunStrategyBase):
    """
    First injection of gp evolved strategies

    """

    def __init__(self, config: GpRunStrategyBaseConfig, ev_strategy=None) -> None:

        super().__init__(config)

        if ev_strategy:
            self.ev_strategy = ev_strategy

        self.p = Params()
        self.verbosity = self.p.naut_dict['VERBOSITY']
        
    def __main__():
        return 1

    def check_triggers(self, blank = ""):

            if self.verbosity: # note, this will log for every bar checked
                logging.debug(
                    f"GpRunStrategyInject.check_triggers: {self.ev_strategy}")

            # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            # THE BELOW IS DIRECTLY FROM EMACROSS
            # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''

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
