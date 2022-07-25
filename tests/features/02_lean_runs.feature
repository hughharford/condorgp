Feature: Lean runs and outputs results
  As a fitness function,
  I want to use Lean in a container,
  So that I can run almost endless fitness tests.

    Scenario: Basic Lean run
    Given quantconnect/lean:latest docker image
    And lean_runner py file with RunLean class and run_lean_via_CLI method
    When RunLean.run_lean_via_CLI is run
    Then Lean/Backtests files are updated
