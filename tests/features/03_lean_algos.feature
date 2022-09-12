# IndBasicAlgo1
# IndBasicAlgo2

Feature: Lean tests each evolved individual
  As a fitness function,
  I want to Lean to run each fitness test,
  So that I can get a fitness score for each.

  Scenario Outline: Lean tests each individual
    Given a Lean container ready to run
    And an evolved "<input_ind>" is specified
    When Lean runs the "<input_ind>" via the CLI
    Then the "<output_ind>" is found
    And the "<input_ind>" algorithm is tidied away

    Examples:
      | input_ind            |   output_ind              |
      | IndBasicAlgo2        |   hsth_testing           |
      | IndBasicAlgo1        |   IndBasicAlgo1           |
