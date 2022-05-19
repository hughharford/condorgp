# @condor_cells
Feature: Condor cells run as required
  As a condorGP instance,
  I want to run cells according to their intended operation,
  So that they operate as living cells.


  # @add
  Scenario Outline: Add a cell
    Given the nest has "<initial>" cells
    When "<some>" cells are added to the nest
    Then the nest contains "<total>" cells

    Examples:
      | initial | some | total |
      | 0       | 3    | 3     |
      | 3       | 4    | 7     |
      | 7       | 5    | 12    |
