Feature: GpControl class achieves various functionality
  As a gp controller,
  GpControl needs to set and control various characteristics,
  To ensure setups are run.

  # ~~~~~~~~~~~~~~~~~~~ 1/3 ~~~~~~~~~~~~~~~~~~~~~~~

  # Scenario Outline: GpControl can set different psets as needed
  #   Given a specific pset is needed
  #   When GpControl gets a requirement for "<pset_input>"
  #   And GpControl is checked
  #   Then the pset returned is not the same as the base_pset
  #   And the pset returns contains "<primitive_name>"

  #   Examples:
  #     | pset_input      |  primitive_name   |
  #     | test_pset5a      |  vmul             |
  #     | test_pset5b      |  vadd             |

  # ~~~~~~~~~~~~~~~~~~~ 2/3 ~~~~~~~~~~~~~~~~~~~~~~~

  Scenario Outline: test psets can output specific text to condor log
    Given a specific test pset "<test_5c_psets>"
    When provided the "<arg_input>"
    Then the result is "<text_output>"

    Examples:
      | arg_input     | test_5c_psets   |  text_output  |
      | hello_world   | test_pset5c     |  hello_world  |

  # ~~~~~~~~~~~~~~~~~~~ 3/3 ~~~~~~~~~~~~~~~~~~~~~~~

  # # NB.
  # # irrelevant work to establish direct inputs to the gp process
  # # inputs to the actual fitness function via Lean in any case

  # Scenario Outline: test pset D can inputted specific text
  #   Given another specific test pset "<test_5d_psets>"
  #   When a run is done
  #   Then 1st result is "<t1>"
  #   And 2nd result is

  #   Examples:
  #     | test_5d_psets   |  t1                 |
  #     | test_pset5d     |  injected_code_test |
