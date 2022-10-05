Feature: Deap basic operations
  As a package with genetic programming functionality,
  I want to Deap to undertake a range of basic gp functions,
  So that tested gp operations can be relied upon.

  Scenario Outline: Deap instanciation includes functions
    Given Deap is setup
    When an instance of Deap is instantiated
    And the functions are listed
    Then the fundamental functions are found

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Examples:
    #   | input_ind       |   output_ind       |   ROI_over_MDD_value    |
    #   | IndBasicAlgo2   |   IndBasicAlgo2    |   110.382               |
    #   | IndBasicAlgo1   |   IndBasicAlgo1    |   74.891                |
