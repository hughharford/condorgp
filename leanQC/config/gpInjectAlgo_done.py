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
# both these imports work in theory, but CAUSES ERRORS WITH C# python wrapper:
#### # AlgorithmFactory/Python/Wrappers/AlgorithmPythonWrapper.cs:line 74 in main.py: line 19
#### #  No module named 'condorgp'
# from condorgp.gp.gp_control import GpControl

# this didn't work, condorgp path already in sys.path:
# import site
# import sys
# site.addsitedir('../../condorgp')  # Always appends to end
# # /home/hsth/code/hughharford/condorgp/condorgp
# print(sys.path)

# import condorgp.gp.gp_functions


### <summary>
### Basic template framework algorithm uses framework components to define the algorithm.
### </summary>
### <meta name="tag" content="using data" />
### <meta name="tag" content="using quantconnect" />
### <meta name="tag" content="trading and orders" />
class gpInjectAlgo(QCAlgorithm):
    '''Basic template framework algorithm uses framework components to define the algorithm.'''

    ## INJECT GP CODE HERE:

    def cgp_set_alpha(self):
        return HistoricalReturnsAlphaModel()
    def newly_injected_code(self):
        gpf = GpFunctions()
        gpf.print_out_please()

    def Initialize(self):
        ''' Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''


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

        # PUT IN CODE HERE >>>>>>>>>>>>>>>>>>>>>>>
        # self.SetAlpha(ConstantAlphaModel(InsightType.Price, InsightDirection.Up, timedelta(minutes = 20), 0.025, None))
        try:
            self.SetAlpha(self.cgp_set_alpha())
        except BaseException as e:
            self.Error(f'<< CONDOR INJECT-CODE ERROR >> {str(e)}')

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

    # def OnData(self, slice):
    #     ''' trialling printing the incoming data slice'''
    #     self.newly_injected_code(slice) # TEMP_LINE_test_06
