Feature: GpControl's evolved code be runnable, be semantically ok
  As a gp algorithm,
  Evolved code created by GpControl must be able to run,
  To ensure the code is of use.

  Scenario Outline: Evolved code can be run
    Given GpControl with "<pset_input_08>"
    When 08 Lean run with enough pop & gen
    Then 08 fitness is above zero
    And 08 shows fitness increasing

    Examples:
      | pset_input_08   |
      | test_pset8a     |
      | test_pset8b     |
