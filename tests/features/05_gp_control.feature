Feature: GpControl class achieves various functionality
  As a gp controller,
  GpControl needs to set and control various characteristics,
  To ensure setups are run.

  Scenario Outline: GpControl can set different psets as needed
    Given a specific pset is needed
    When GpControl receieves a requirement for a "<pset_input>"
    And a Deap run is conducted
    Then the pset returned is not the same as the base_pset
    And the pset returns contains "<pset_name>"

    Examples:
      | pset_input      |  pset_name    |
      | psetA           |  mul          |
      | psetB           |  add          |
