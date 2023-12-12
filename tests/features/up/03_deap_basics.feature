Feature: Deap basic operations
  As a package with genetic programming functionality,
  I want to Deap to undertake a range of basic gp functions,
  So that tested gp operations can be relied upon.

  Scenario Outline: Deap instanciation includes functions
    Given Deap is setup
    When an instance of Deap is instantiated
    And the functions are added
    Then the fundamental functions are found
