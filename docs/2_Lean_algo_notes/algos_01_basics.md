
# OVERVIEW:
# See ____ https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/overview

# https://www.quantconnect.com/docs/v2/writing-algorithms/initialization

class AnyAlgoName(QCAlgorithm):
    '''Basic template framework algorithm uses framework components to define the algorithm.'''

    def Initialize(self):
        ''' Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        self.SetStartDate(2013, 1, 5)                  # Set start date to January 5, 2013
        self.SetEndDate(2015, 1, 5)                    # Set end date to January 5, 2015
        self.SetEndDate(datetime.now() - timedelta(7)) # Set end date to last week

        self.SetAccountCurrency("BTC") # default USD,

        self.SetCash(100000)       # Set the quantity of the account currency to 100,000
        self.SetCash("BTC", 10)    # Set the Bitcoin quantity to 10
        self.SetCash("EUR", 10000) # Set the EUR quantity to 10,000

# see https://www.quantconnect.com/docs/v2/our-platform/live-trading/brokerages
        # self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Cash)


# paper trading:
# see https://www.quantconnect.com/docs/v2/our-platform/live-trading/brokerages/quantconnect-paper-trading
        # The QuantConnect Paper Trading brokerage supports cash and margin accounts:
        self.SetBrokerageModel(BrokerageName.QuantConnectBrokerage, AccountType.Cash)
        # self.SetBrokerageModel(BrokerageName.QuantConnectBrokerage, AccountType.Margin)

        # WARMUP
        # Wind time back 7 days from the start date
        self.SetWarmUp(timedelta(7))

        # Feed in 100 trading days worth of data before the start date
        self.SetWarmUp(100, Resolution.Daily)

#         Post Initialization

# After the Initialize method, the PostInitialize method performs post-initialization routines, so don't override it. To be notified when the algorithm is # ready to begin trading, define an OnWarmUpFinished method. This method executes even if you don't set a warm-up period.
      def OnWarmUpFinished(self) -> None:
        self.Log("Algorithm Ready")

# ON DATA
      def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.


# API REFERENCE for QCalgorithm methods:
# see https://www.quantconnect.com/docs/v2/writing-algorithms/api-reference and click indicators

# Algorithm Framework
# SEE https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/overview


# ALPHA models
# These provide the insights on which trades are made
# see https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/alpha/key-concepts
# Supported built in Alpha models:
# see https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/alpha/supported-models

self.AddAlpha(NullAlphaModel())
self.AddAlpha(ConstantAlphaModel(type, direction, period))
self.AddAlpha(HistoricalReturnsAlphaModel())
self.AddAlpha(EmaCrossAlphaModel())
self.AddAlpha(MacdAlphaModel())
self.AddAlpha(RsiAlphaModel())

The Alpha model predicts market trends and signals the best moments to trade. These signals, or Insight objects, contain the Direction, Magnitude, and Confidence of a market prediction and the suggested portfolio Weight. You should generate insights on the set of assets provided by the Universe Selection model and only generate them when your predictions change.

  Multi-Alpha Algorithms
      You can add multiple Alpha models to a single algorithm and generate Insight objects with all of them.



# Model names
#           To ensure your Alpha model is compatible with all Portfolio Construction models, assign a unique name to your Alpha model.

# Model Structure:

# Algorithm framework model that produces insights
      class RsiAlphaModel(AlphaModel):
          Name = "RsiAlphaModel"

          def Update(self, algorithm: QCAlgorithm, data: Slice) -> List[Insight]:
              # Updates this Alpha model with the latest data from the algorithm.
              # This is called each time the algorithm receives data for subscribed securities
              # Generate insights on the securities in the universe.
              insights = []
              return insights

          def OnSecuritiesChanged(self, algorithm: QCAlgorithm, changes: SecurityChanges) -> None:
              # Security additions and removals are pushed here.
              # This can be used for setting up algorithm state.
              # changes.AddedSecurities
              # changes.RemovedSecurities
              pass


# the PORTFOLIO CONSTRUCTION MODEL
# The Portfolio Construction model consumes the Insight objects from the Alpha model. It's up to the Portfolio Construction model to define how Insight objects are converted into PortfolioTarget objects.
# SEE _________ https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/portfolio-construction/key-concepts

    The Portfolio Construction model receives Insight objects from the Alpha model and creates PortfolioTarget objects for the Risk Management model. A PortfolioTarget provides the number of units of an asset to hold.

# Supported PORTFOLIO CONSTRUCTION MODELS:
# See _________ https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/portfolio-construction/supported-models


# RISK MANAGEMENT OPTIONS
# SEE ____ https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/risk-management/key-concepts
# Supported models:
# ______________  https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/risk-management/supported-models

# EXECUTION
# See ____ https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/execution/key-concepts
# Supported execution models:
#                    https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/execution/supported-models
