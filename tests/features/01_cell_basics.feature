# @condor_cells
Feature: Condor cells run as required
  As a condorGP instance,
  I want to run cells according to their intended operation,
  So that they operate as living cells.


  # @add
  Scenario Outline: Add cells
    Given the nest has "<initial>" cells
    When "<some>" cells are added to the nest
    Then the nest contains "<total>" cells

    Examples:
      | initial | some | total |
      | 0       | 3    | 3     |
      | 3       | 4    | 7     |
      | 7       | 5    | 12    |

  Scenario Outline: Remove cells
    Given the existing nest has "<initial>" cells
    When "<some>" cells are removed
    Then the nest now contains "<total>" cells

    Examples:
      | initial | some | total |
      | 12      | 8    | 4     |
      | 4       | 4    | 0     |
