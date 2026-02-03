Feature: Simple usage of Nautilus by Deap, connecting the two
  As an evoluationary algorithm,
  Deap needs to use Nautilus to evaluate,
  To test each invidual.

  Scenario Outline: Nautilus is run and reports success and fitness
    Given a setup with Deap using Nautilus
    When a short Deap run is conducted
    Then the result is not "<not_found_code>"
    And the result is not "<nan_code>"

    Examples:
      | input_ind  |   not_found_code    |  nan_code   |
      | default    |   111000            |  22000      |
