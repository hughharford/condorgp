Feature: GpControl's evolved code must affect Lean functionality
  As a gp algorithm,
  Evolved code created by GpControl needs to alter various characteristics,
  To ensure genuine fitness can be established.

  Scenario Outline: Evolved code shows Lean logged differences
    Given GpControl is run with "<pset_input>"
    When the injected algo is varied
    Then Lean o/p is NOT "<RoMDD>"

    Examples:
      | pset_input       |  RoMDD      |
      | test_psetEa      |  110.382    |
      | test_psetEb      |  110.382    |

# the prime one to alter is the:
# self.SetAlpha()
