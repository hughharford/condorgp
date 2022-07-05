Feature: Lean runs and outputs results
  As a fitness function,
  I want to use Lean in a container,
  So that I can run endless fitness tests.

    Scenario: Basic Lean run
    Given lean:latest docker image
    And run_docker.sh file
    When run_docker.sh is run
    Then leanQC/results files are updated

  # Scenario Outline: Configured Lean Run
  #   Given the nest has "<initial>" cells
  #   When "<some>" cells are added to the nest
  #   Then the nest contains "<total>" cells

  #   Examples:
  #     | initial | some | total |
  #     | 0       | 3    | 3     |
  #     | 3       | 4    | 7     |
  #     | 7       | 5    | 12    |
