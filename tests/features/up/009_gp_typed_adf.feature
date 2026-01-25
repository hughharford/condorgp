Feature: GpControl's typed evolved code must be runnable
  As a gp algorithm,
  Evolved code must be typed, include ADFs, and be able to run,
  To ensure the code is of use.

  Scenario Outline: Evolved code can be run including ADFs
    Given GpControl with "<pset_ADF>"
    When a short ADF run is made with "<evaluator>"
    Then the fitness is not zero

    Examples:
      | pset_ADF            |   evaluator          |
      | naut_pset_02_adf    |   eval_nautilus      |
