Feature: GpControl's evolved code must affect Nautilus functionality
  As a gp algorithm,
  Evolved code created by GpControl needs to alter various characteristics,
  To ensure genuine fitness can be established.

  Scenario Outline: Evolved code shows Nautilus logged differences
    Given GpControl is run with "<pset_input>"
    When the evolved code is used
    Then Nautilus o/p is NEITHER "<expected_A>"
    And NOR is the Nautilus o/p "<expected_B>"

    Examples:
      | pset_input       |  expected_A         |   expected_B           |
      | naut_pset_01     |  -21.496631427091   |   -16.160361991815254  |
