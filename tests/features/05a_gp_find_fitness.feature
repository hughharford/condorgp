Feature: Finding the fitness after every test is critcal
  As part of a gp system,
  gp_functions.find_fitness needs to correct find fitness from logs,
  To ensure evolution is effective.

  Scenario Outline: find_fitness can correctly find fitness from logs
    Given the test_find_fitness_1.json
    When find_fitness gets fitness for "<naut_runner>"
    And the runner name is "<runner_name>"
    Then the fitness found is "<sharpe_ratio>"
    And the fitness found is "<risk_return>"

    Examples:
      | naut_runner     | runner_name | sharpe_ratio        | risk_return          |
      | naut_02_egFX.py | naut-run-02 | 15.966514528587545  | 0.0925170264669847   |
      | naut_03_egFX.py | naut-run-03 | -21.49663142709111  | -0.09001786197454079 |
      | naut_04_egFX.py | naut-run-04 | -16.160361991815254 | -0.5005168529510061  |

  Scenario Outline: find_fitness finds the latest fitness from logs
    Given the test_find_fitness_2.json
    When find_fitness gets the latest fitness for "<naut_runner>"
    And checks the runner name is "<runner_name>"
    Then the latest fitness found is "<sharpe_ratio>"
    # i.e. doesn't get confused by earlier naut-run-04 entries x 2
    # or other naut-run-02 entries with different earlier outputs x2

    Examples:
      | naut_runner     | runner_name | sharpe_ratio       |
      | naut_02_egFX.py | naut-run-02 | 15.966514528587545 |
      | naut_03_egFX.py | naut-run-03 | -21.49663142709111 |
