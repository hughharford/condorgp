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

  Scenario Outline: test psets can output specific text to condor log
    Given a specific test pset "<test_C_psets>"
    When provided the "<arg_input>"
    Then the result is "<text_output>"

    Examples:
      | arg_input     | test_C_psets    |  text_output  |
      | hello_world   | test_psetC      |  hello_world  |

  # Scenario Outline: test pset D can output specific text
  #   Given a specific test pset "<test_D_psets>"
  #   When a run is done
  #   Then 1st result is "<t1>"
  #   And 2nd result is

  #   Examples:
  #     | test_D_psets    |  t1                 |
  #     | test_psetC      |  hello_world        |
  #     | test_psetCi     |  hi_hi_hi_hi        |
