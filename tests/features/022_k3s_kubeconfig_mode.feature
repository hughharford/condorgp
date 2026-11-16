@G_kubeconfig
Feature: The k3s kubeconfig is readable by its owner only
  As the owner of a k3s cluster
  I want the admin kubeconfig written with mode 600
  So that no other user on the hub can read cluster-admin credentials

  Scenario: No install command or config makes the kubeconfig readable by others
    Given the repository files
    When I read every write-kubeconfig-mode setting
    Then each one is 600 or 0600

  Scenario: The k3s server config in the repo sets the mode to 0600
    Given the repository files
    When I read the k3s server config example
    Then it sets write-kubeconfig-mode to "0600"
    And it does not set it anywhere else to a different value

  Scenario: The install notes tell the user how to run kubectl with a 0600 file
    Given the repository files
    When I read the k3s hub-and-spoke guide
    Then it explains how to use a 0600 kubeconfig and why 644 must not be used

  Scenario: A known-bad k3s setup proves the kubeconfig checks can fail
    Given the bad k3s config, install command and guide kept in the test data
    Then they say plainly that they are fake, deliberately bad examples
    And every kubeconfig check fails on them

  Scenario: The checks notice when the canary stops being bad
    Given the bad k3s config, install command and guide kept in the test data
    When I fix or empty a copy of the canary
    Then the canary guard rejects that copy

  Scenario: The canary never reaches the real checks
    Given the bad k3s config, install command and guide kept in the test data
    Then the repository scan skips all three
