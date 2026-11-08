@E_dashboard
Feature: The cluster dashboard is maintained, read-only and not exposed
  As someone running a cluster on a network I do not fully control
  I want a supported dashboard that can only look, and that only my own machine can reach
  So that a stolen dashboard token or an open port never hands over the cluster

  Scenario: The retired Kubernetes Dashboard is no longer deployed
    Given the repository files
    When I search the manifests and scripts for the retired Kubernetes Dashboard
    Then it is not installed anywhere

  Scenario: The replacement dashboard is pinned to a released version
    Given the dashboard manifest
    Then its image has an explicit version tag and is not latest

  Scenario: The dashboard pod is hardened
    Given the dashboard manifest
    Then the container runs non-root, without privilege escalation or capabilities, on a read-only filesystem with the default seccomp profile
    And it has CPU and memory limits and mounts no host path

  Scenario: The dashboard is only reachable inside the cluster
    Given the dashboard manifest
    Then its Service is ClusterIP and nothing in the manifests exposes it through an Ingress

  Scenario: The dashboard pod's own account has no permissions
    Given the dashboard manifest
    Then no binding anywhere grants anything to the dashboard's service account

  Scenario: The login account can only read, and cannot read Secrets
    Given the repository files
    When I read every RBAC object that mentions a dashboard account
    Then no dashboard account is bound to cluster-admin, admin or edit
    And the viewer account is bound to the built-in view role
    And every extra rule it has is get, list or watch and none touches Secrets

  Scenario: No script creates an administrator account for the dashboard
    Given the repository files
    When I read every kubectl command that creates a role binding
    Then none of them binds cluster-admin

  Scenario: Port-forwards and proxies are bound to loopback only
    Given the repository files
    When I read every kubectl port-forward and kubectl proxy command
    Then none binds an address other than 127.0.0.1, localhost or ::1

  Scenario: The scripts and Makefile open the new dashboard, not the retired one
    Given the repository files
    When I read the dashboard commands in the Makefile
    Then the dashboard target port-forwards the headlamp service and logs in with a short-lived token

  Scenario: The dashboard manifests are wired together
    Given the dashboard manifest
    Then the Service selects the Deployment's pods and targets its named container port
    And the viewer account lives in the dashboard's namespace
