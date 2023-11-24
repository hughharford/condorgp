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
    And the result: "<ROI_over_MDD_value>" is reported
    And the "<input_ind>" algorithm is tidied away

    Examples:
      | input_ind       |   output_ind       |   ROI_over_MDD_value    |
      | IndBasicAlgo2   |   IndBasicAlgo2    |   110.382               |
      | IndBasicAlgo1   |   IndBasicAlgo1    |   74.891                |
