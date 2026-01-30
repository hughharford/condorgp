Feature: CondorGp's evolutions need powerful resources to evolve many times
  As a gp algorithm many evolutions are needed,
  Resources must be allocated, run, and return results effectively
  To allow backtesting.

# operate microk8s to run many resources effectively
  Scenario Outline: When microk8s is started
    Given the initial k8s setup
    When the cluster has settled
    Then a green status is found for <deployment-for-test>

    Examples:
      | deployment-for-test     |
      | cgp-master              |
      | cgp-worker-1            |
      | cgp-grafana             |
      | cgp-database            |
      | cgp-rabbitmq            |
