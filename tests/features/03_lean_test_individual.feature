Feature: Lean tests each evolved individual
  As a fitness function,
  I want to Lean to run each fitness test,
  So that I can get a fitness score for each.

  Scenario Outline: Lean tests each individual
    Given a Lean container ready to run
    And an evolved "<individual>" is specified
    When Lean runs
    Then the "<individual>" is used

    Examples:
      | individual          |
      | IndBasicAlgo1       |
      | IndBasicAlgo2       |
