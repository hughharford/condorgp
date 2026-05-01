Feature: Start k3d ecosystem for CondorGP
  As an operator preparing evolutionary runs
  I need the local k3d environment to start cleanly
  So CondorGP services are ready for backtesting.

  Scenario: Cluster starts from a stopped state
    Given k3d installs are in place and cluster is not started
    When the cluster is started
    Then the cluster status is healthy
    And all CondorGP namespaces are available

  Scenario: Cluster starts and becomes ready
    Given the initial k3d setup
    When the cluster is started
    Then the cluster status is healthy
    And all CondorGP namespaces are available

  Scenario: Kubernetes dashboard is up and available
    Given the k3d cluster has settled
    When the kubernetes dashboard is deployed from repo manifests
    Then the kubernetes dashboard deployment is ready
    And the kubernetes dashboard service has ready endpoints
    And the kubernetes dashboard is available at the configured URL

  Scenario Outline: Core services report ready status
    Given the k3d cluster has settled
    Then deployment "<deployment>" reports ready

    Examples:
      | deployment    |
      | cgp-master    |
      | cgp-worker-1  |
      | cgp-grafana   |
      | cgp-database  |
      | cgp-rabbitmq  |
