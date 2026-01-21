Feature: GpControl's evolved code must improve fitness
  As a gp algorithm,
  Evolved code fitness must improve - fitness max in this case,
  To ensure positive direction is ensured.

  Scenario Outline: Evolved code shows fitness improvement
    Given GpControl is run with "<pset>"
    When run with evaluator "<evaluator>"
    Then max fitness is static or improves over generations

  Examples:
    |  pset                  |   evaluator          |
#    |  naut_pset_01          |   eval_nautilus      |
    |  test_adf_symbreg_pset |   evalSymbRegTest    |
