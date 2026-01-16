Feature: CondorGp's evolved cell code needs evaluation
  As a gp algorithm running with living cell structures,
  Evolved cell code must be structured correctly,
  To allow evaluation via scoring.

  Scenario Outline: Evolved living cell code is run
    Given CellEvaluator and no cells
    When an evaluation is made
    Then zero results are returned
    And this is handled

#  Scenario Outline: One living cell is run
#    Given CellEvaluator and one cell
#    When an evaluation is made
#    Then one result are returned
#    And this is handled

#  Scenario Outline: Three living cells code are run
#    Given CellEvaluator, 3 cells and a database
#    When an evaluation is made
#    Then 3 results are returned
#    And these are stored in the database
