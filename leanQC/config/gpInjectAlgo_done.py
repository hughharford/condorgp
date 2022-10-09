# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import numpy as np

from AlgorithmImports import *

### <summary>
### Basic template framework algorithm uses framework components to define the algorithm.
### </summary>
### <meta name="tag" content="using data" />
### <meta name="tag" content="using quantconnect" />
### <meta name="tag" content="trading and orders" />
class gpInjectAlgo(QCAlgorithm):
    '''Basic template framework algorithm uses framework components to define the algorithm.'''

    ## INJECT GP CODE HERE:

    def newly_injected_code(self):
        self.Debug("eval_test_D: injected_code_test {0}")

    def Initialize(self):
        ''' Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        self.newly_injected_code() # TEMP LINE

        # Set requested data resolution
        self.UniverseSettings.Resolution = Resolution.Hour

        self.SetStartDate(2013,10,7)   #Set Start Date
        self.SetEndDate(2013,10,11)    #Set End Date
        self.SetCash(1_000_000)           #Set Strategy Cash
        
        # Find more symbols here: http://quantconnect.com/data
        # Forex, CFD, Equities Resolutions: Tick, Second, Minute, Hour, Daily.
        # Futures Resolution: Tick, Second, Minute
        # Options Resolution: Minute Only.
        symbols = [ Symbol.Create("SPY", SecurityType.Equity, Market.USA) ]

        # set algorithm framework models
        self.SetUniverseSelection(ManualUniverseSelectionModel(symbols))
        self.SetAlpha(ConstantAlphaModel(InsightType.Price, InsightDirection.Up, timedelta(minutes = 20), 0.025, None))

        # We can define who often the EWPCM will rebalance if no new insight is submitted using:
        # Resolution Enum:
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel(Resolution.Daily))
        # timedelta
        # self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel(timedelta(2)))
        # A lamdda datetime -> datetime. In this case, we can use the pre-defined func at Expiry helper class
        # self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel(Expiry.EndOfWeek))

        self.SetExecution(ImmediateExecutionModel())
        self.SetRiskManagement(MaximumDrawdownPercentPerSecurity(0.01))

        self.Debug("numpy test >>> print numpy.pi: " + str(np.pi))

    def OnOrderEvent(self, orderEvent):
        if orderEvent.Status == OrderStatus.Filled:
            self.Debug("Purchased Stock: {0}".format(orderEvent.Symbol))
