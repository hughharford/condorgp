Feature: GpControl's evolution improves fitness over time
  As a gp algorithm, considerable time is taken evolved code
  This means checkpointing and restarting are essential,
  To ensure restarting from zero isn't needed every time.

  Scenario Outline: Evolved populations can be checkpointed
    Given gp_deap_adf.GpDeapAdfCp
    When a 6 generation run with checkpoints every 3 is made
    Then the checkpoint file is created at generation 3
    And the checkpoint is updated at generation 6
