Feature: GpControl's evolved code must improve fitness
  As a gp algorithm,
  Evolved code fitness must improve - fitness max in this case,
  To ensure positive direction is ensured.

  Scenario Outline: Evolved code shows fitness improvement
    Given GpControl is run with test_pset7aTyped
    When the injected algo runs with 7aT
    Then fitness improves over the generations run
