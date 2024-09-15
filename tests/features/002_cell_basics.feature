Feature: CondorGp's evolved cell code needs basic operations
  As a gp algorithm with living cell structures,
  Evolved cells must be able to be added and removed, and a count kept
  To allow sensible management of cells.

# birth of a cell
  Scenario Outline: A cell is added
    Given no cells
    When a cell is born
    Then an object of type Cell is added
    And with first birth cell count is 1

# death of a cell
  Scenario Outline: One living cell is run
    Given 1 extant cell
    When the cell is removed
    Then there are 0 objects of type Cell
    And with first removal cell count is 0 again


# failed cell birth

# failed cell death
