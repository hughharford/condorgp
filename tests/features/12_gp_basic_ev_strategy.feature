Feature: CondorGp's evolved code is immediately most effective as a strategy
  As a gp algorithm running with Nautilus,
  Evolved code must be structured as a Nautilus strategy,
  To ensure the ongoing evolution is well targeted.

  Scenario Outline: Evolved code can be run as a strategy
    Given GpControl with naut_06_gp_strategy
    When a first evolved strategy run is made
    Then the initial strategy fitness is not zero
