Feature: Simple usage of Lean by Deap, connecting the two
  As an evoluationary algorithm,
  Deap needs to use Lean to evaluate,
  To test each invidual.

  Scenario Outline: Lean is run and reports success and fitness
    Given a setup with Deap using Lean
    When Deap specs Lean to run "<input_ind>"
    Then the "<output_ind>" is found
    And the result: "<ROI_over_MDD_value>" is reported
    And the "<input_ind>" algorithm is tidied away

    Examples:
      | input_ind       |   output_ind       |   ROI_over_MDD_value    |
      | IndBasicAlgo1   |   IndBasicAlgo1    |   74.891                |
