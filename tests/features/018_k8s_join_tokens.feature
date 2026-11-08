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
