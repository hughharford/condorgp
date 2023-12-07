#!/usr/bin/env python3
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

# copied in full directly from:
# https://github.com/nautechsystems/nautilus_trader/blob/master/examples/backtest/fx_ema_cross_audusd_bars_from_ticks.py

import time
from decimal import Decimal

import pandas as pd

from nautilus_trader.backtest.node import BacktestEngine
from nautilus_trader.backtest.node import BacktestEngineConfig
from nautilus_trader.backtest.modules import FXRolloverInterestConfig
from nautilus_trader.backtest.modules import FXRolloverInterestModule
from nautilus_trader.examples.strategies.ema_cross import EMACross
from nautilus_trader.examples.strategies.ema_cross import EMACrossConfig
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.enums import AccountType
from nautilus_trader.model.enums import OmsType
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Money
from nautilus_trader.persistence.wranglers import QuoteTickDataWrangler
from nautilus_trader.test_kit.providers import TestDataProvider
from nautilus_trader.test_kit.providers import TestInstrumentProvider

from nautilus_trader.config import LoggingConfig
from condorgp.evaluation.overloaded_nt.cgp_providers import *

# CGP addition
from condorgp.evaluation.get_strategies import GetStrategies

class NautRunsEvolved:

    def __init__(self):
        pass

    def main(self, evolved_config=""):
        # Configure backtest engine
        config = BacktestEngineConfig(
            trader_id="BACKTESTER-001-naut-run-05",
            logging=LoggingConfig(log_level="ERROR",
                log_level_file="INFO",
                log_file_format="json",
                log_file_name="nautilus_log",
                log_directory="condorgp/util/logs/",
                log_component_levels={ "Portfolio": "ERROR" }),
        )

        # Build the backtest engine
        engine = BacktestEngine(config=config)

        # Optional plug in module to simulate rollover interest,
        # the data is coming from packaged test data.
        provider = CondorGPTestDataProvider()
        interest_rate_data = provider.read_csv("short-term-interest.csv")
        config = FXRolloverInterestConfig(interest_rate_data)
        fx_rollover_interest = FXRolloverInterestModule(config=config)

        # Add a trading venue (multiple venues possible)
        SIM = Venue("SIM")
        engine.add_venue(
            venue=SIM,
            oms_type=OmsType.HEDGING,  # Venue will generate position IDs
            account_type=AccountType.MARGIN,
            base_currency=USD,  # Standard single-currency account
            starting_balances=[Money(1_000_000, USD)],  # Single-currency or multi-currency accounts
            modules=[fx_rollover_interest],
        )

        # Add instruments
        AUDUSD_SIM = TestInstrumentProvider.default_fx_ccy("AUD/USD", SIM)
        engine.add_instrument(AUDUSD_SIM)

        # Add data
        wrangler = QuoteTickDataWrangler(instrument=AUDUSD_SIM)
        ticks = wrangler.process(provider.read_csv_ticks("truefx/audusd-ticks.csv"))
        engine.add_data(ticks)

        # CGP CHANGE HERE
        if evolved_config:
            gp_strategy = GetStrategies(
                instrument = AUDUSD_SIM).get_strategy(config_ev=evolved_config)
        else:
            # seperated out - see get_strategies.py
            gp_strategy = GetStrategies(
                instrument = AUDUSD_SIM).get_strategy()

        # add the strategy
        engine.add_strategy(strategy=gp_strategy)

        # CGP COMMENTED HERE
        # time.sleep(0.1)
        # input("Press Enter to continue...")

        # Run the engine (from start to end of data)
        engine.run()

        # Optionally view reports
        with pd.option_context(
            "display.max_rows",
            100,
            "display.max_columns",
            None,
            "display.width",
            300,
        ):
            print(engine.trader.generate_account_report(SIM))
            print(engine.trader.generate_order_fills_report())
            print(engine.trader.generate_positions_report())

        # For repeated backtest runs make sure to reset the engine
        engine.reset()

        # Good practice to dispose of the object when done
        engine.dispose()

if __name__ == "__main__":
    rne = NautRunsEvolved()
    rne.main()
