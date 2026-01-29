Feature: Nautilus tests each evolved individual
  As a fitness function,
  I want to Nautilus to run each fitness test,
  So that I can get a fitness score for each.

  Scenario Outline: Nautilus tests each individual
    Given a Nautilus setup ready to run
    And an evolved "<input_ind>" is specified
    When Nautilus runs the "<input_ind>"
    Then the "<output_ind>" is found
    And the result: "<expected_value>" is reported

    Examples:
      | input_ind        |   output_ind   |   expected_value      |
      | naut_03_egFX.py  |   naut-run-03  |   -7.1565691385547385 |
      | naut_04_egFX.py  |   naut-run-04  |   -15.874507866387544 |
