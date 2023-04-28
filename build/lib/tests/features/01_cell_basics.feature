Feature: Condor cells run as required
  As a condorGP instance,
  I want to run cells according to their intended operation,
  So that they operate as living cells.


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

  # @cellidchange
  # Scenario: Cell id change
  #   Given a pre-created cell with <initial_id>
  #   When the cell id is changed to <text_to_change_to>
  #   Then the new cell id is <intended_id>

  #   Examples:
  #     | initial_id | text_to_change_to | intended_id  |
  #     | id_one     | new_id_1          | new_id_1     |
  #     | id_two     | new_id_2          | new_id_2     |
