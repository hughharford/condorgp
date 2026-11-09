@B_tokens
Feature: Cluster join tokens are never committed
  As the owner of a public repository that bootstraps a cluster
  I want kubeadm and k3s join credentials kept out of it
  So that nobody can join a machine to my cluster or reach its control plane

  Scenario: No kubeadm bootstrap token is committed
    Given the repository files
    When I search for kubeadm bootstrap tokens
    Then none is found

  Scenario: No k3s or Docker Swarm join token is committed
    Given the repository files
    When I search for k3s and Docker Swarm join tokens
    Then none is found

  Scenario: Join commands in the notes use placeholders
    Given the repository files
    When I read every join command and token argument
    Then each token, CA hash and certificate key is a placeholder

  Scenario: Captured kubeadm logs carry no certificate key
    Given the repository files
    When I search the files for kubeadm certificate keys
    Then none is found

  Scenario: Token and admin credential files cannot be committed by accident
    Given the repository ignore rules
    Then join tokens and admin kubeconfigs are ignored

  Scenario: The guide explains how to handle tokens going forward
    Given the secrets management guide
    Then it covers separate agent tokens, token files, rotation, deleting kubeadm tokens and shell history

  Scenario: A known-bad canary proves the token checks can fail
    Given the token canary kept in the test data
    Then it says plainly that every value in it is fake
    And every kind of join credential the checks look for is found in it

  Scenario: The checks notice when the canary stops being bad
    Given the token canary kept in the test data
    When I redact, empty or strip one kind of credential from a copy
    Then the canary guard rejects that copy

  Scenario: The canary never reaches the real checks
    Given the token canary kept in the test data
    Then the repository scan skips it
