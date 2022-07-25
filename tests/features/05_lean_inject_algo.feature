Feature: Lean reports results for each evolved individual
  As a fitness function,
  I want to inject evolved code and get a different result accordingly,
  So that I can usefully evolve and test each invidual.

  Scenario Outline: Lean reports results for injected individual
    Given a Lean container ready to run
    And a Lean algo wrapper that works
    And a text of "<evolved_code>" is injected
    When Lean runs the "<input_ind>" via the CLI
    Then the result: "<Return_Over_Maximum_Drawdown>" is reported
    And the fitness function demonstrates this result

    Examples:
      | evolved_code        | input_ind       | Return_Over_Maximum_Drawdown  |
      | file_with_gp_code   | gpInjectAlgo1   | 999999                        |
