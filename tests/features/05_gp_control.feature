Feature: GpControl class achieves various functionality
  As a gp controller,
  GpControl needs to set and control various characteristics,
  To ensure setups are run.

  Scenario Outline: GpControl can set different psets as needed
    Given a specific pset is needed
    When GpControl gets a requirement for "<pset_input>"
    And GpControl is checked
    Then the pset returned is not the same as the base_pset
    And the pset returns contains "<primitive_name>"

    Examples:
      | pset_input      |  primitive_name   |
      | test_psetA      |  vmul             |
      | test_psetB      |  vadd             |
