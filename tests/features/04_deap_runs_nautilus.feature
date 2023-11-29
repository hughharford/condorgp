Feature: Simple usage of Nautilus by Deap, connecting the two
  As an evoluationary algorithm,
  Deap needs to use Nautilus to evaluate,
  To test each invidual.

# this previously used ROI over MDD (RoMaD - see investopedia) as this was
# readily available.

  Scenario Outline: Nautilus is run and reports success and fitness
    Given a setup with Deap using Nautilus
    When Deap specs Nautilus to run "<input_ind>"
    And a short Deap run is conducted
    Then the result: "<expected_value>" is found

    Examples:
      | input_ind       |   expected_value          |
      | default         |   -21.496631427091        |
