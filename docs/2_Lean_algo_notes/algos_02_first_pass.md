# FIRST PASS CREATING EVOLVABLE LEAN ALGO:

## Assumptions
### There are lots of moving parts that can be set to constant for now:

  # STATIC _____ Initialize()
      e.g.:
        self.SetStartDate(2013, 1, 5)                  # Set start date to January 5, 2013
        self.SetEndDate(2015, 1, 5)                    # Set end date to January 5, 2015
        self.SetEndDate(datetime.now() - timedelta(7)) # Set end date to last week
        self.SetAccountCurrency("BTC") # default USD,
        self.SetCash(100000)

      # LATER: self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Cash)
      # FOR NOW: The QuantConnect Paper Trading brokerage supports cash and margin accounts:
      self.SetBrokerageModel(BrokerageName.QuantConnectBrokerage, AccountType.Cash)

              # WARMUP
        # Wind time back 7 days from the start date
        self.SetWarmUp(timedelta(7))

        # Feed in 100 trading days worth of data before the start date
        self.SetWarmUp(100, Resolution.Daily)

    # Post Initialization
      # After the Initialize method, the PostInitialize method performs post-initialization routines, so don't override it. To be notified when the algorithm is # ready to begin trading, define an OnWarmUpFinished method. This method executes even if you don't set a warm-up period.

      def OnWarmUpFinished(self) -> None:
        self.Log("Algorithm Ready")

  # VARY HERE ____ Alpha models and other indicators:
    # See all the available methods:
    https://www.quantconnect.com/docs/v2/writing-algorithms/api-reference

    # The Alpha model predicts market trends and signals the best moments to trade. These signals, or Insight objects, contain the Direction, Magnitude, and Confidence of a market prediction and the suggested portfolio Weight. You should generate insights on the set of assets provided by the Universe Selection model and only generate them when your predictions change.

    # Multi-Alpha Algorithms
      You can add multiple Alpha models to a single algorithm and generate Insight objects with all of them.

    # To ensure your Alpha model is compatible with all Portfolio Construction models, assign a unique name to your Alpha model.

    # Use the Framework:

# STATIC _____ PORTFOLIO CONSTRUCTION:
# designed for multi-alpha..
    # SET THIS ONE (assuming >1 alpha models is likely)
    self.SetPortfolioConstruction(BlackLittermanOptimizationPortfolioConstructionModel())

# STATIC _____ Execution Model:
      # There are a range of supported predefined models.
      # Some of them are listed here:
            self.SetExecution(NullExecutionModel())
                # doesn't really count

            self.SetExecution(ImmediateExecutionModel())
            self.SetExecution(SpreadExecutionModel())
            self.SetExecution(StandardDeviationExecutionModel())
  # SET THIS ONE:
      # For the Execution Model, we will set:
            self.SetExecution(ImmediateExecutionModel())
