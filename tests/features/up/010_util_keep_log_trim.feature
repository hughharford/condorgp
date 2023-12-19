Feature: Usage of Nautilus by Deap, creates long logs
  As an evoluationary algorithm,
  Many runs will be made, we need to avoid accumulating massive logs,
  To avoid large files, and their costs.

  Scenario Outline: Deap runs Nautilus and logs are trimmed
    Given a long log file
    When the log file is above "<no_lines>"
    Then the file is less than "<reduced_lines>"

    Examples:
      |   no_lines   |  reduced_lines  |
      |   20000      |  10001          |

#  Scenario Outline: Deap runs Nautilus and logs are backed up
#    Given a specified log file path "<logfilepath>"
#    And the extant number of backups
#    When the number of backups is specified "<no_backups>"
#    Then there is one more than before
#    And there are always less than "<no_backups>"
#
#    Examples:
#      |   no_lines   |  reduced_lines  |
#      |   20000      |  10001          |
#
# see tests/test_data/test_log_backup_orig.txt
