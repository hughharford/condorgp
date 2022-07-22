Feature: Lean reports results for each evolved individual
  As a fitness function,
  I want to Lean to get back a result for each fitness test,
  So that I can usefully evolve inviduals.

  Scenario Outline: Lean reports results for each individual
    Given a Lean container ready to run
    And an evolved "<input_ind>" is specified
    When Lean runs the "<input_ind>" via the CLI
    Then the result: "<Return_Over_Maximum_Drawdown>" is reported
    And the fitness function demonstrates this result

    Examples:
      | input_ind            |   Return_Over_Maximum_Drawdown             |
      | IndBasicAlgo2        |   85.095                                   |
      | IndBasicAlgo1        |   79228162514264337593543950335            |


# Each of the test algos has different dates and cash:

# IndBasicAlgo1 has :
        # self.SetStartDate(2014,10,7)   #Set Start Date
        # self.SetEndDate(2014,10,11)    #Set End Date
        # self.SetCash(1_000_000)           #Set Strategy Cash

# IndBasicAlgo2 has :
        # self.SetStartDate(2013,10,7)   #Set Start Date
        # self.SetEndDate(2013,10,11)    #Set End Date
        # self.SetCash(100_000)           #Set Strategy Cash
