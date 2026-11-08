@D_postgres_init
Feature: The database initialises itself from a ConfigMap
  As the operator of a cluster whose nodes do not share my home directory
  I want the Postgres init script delivered by a ConfigMap
  So that the database starts correctly on any node, whatever path my code lives at

  Scenario: Postgres reads its init script from a ConfigMap, not from a host path
    Given the Postgres manifest
    When I look at how the database Deployment mounts its init scripts
    Then they come from a ConfigMap that exists in the same namespace
    And the Postgres pod mounts no host path

  Scenario: The ConfigMap carries exactly the script Docker Compose uses
    Given the Postgres manifest
    Then the ConfigMap script is identical to scripts/db_init/01-init.sh

  Scenario: The ConfigMap files can be executed by the image's entrypoint
    Given the Postgres manifest
    Then the init volume is mounted with an executable mode

  Scenario: The database pod is given every variable the script needs
    Given the Postgres manifest
    Then the database container receives the Postgres password and the application role settings

  Scenario: Docker Compose still supplies every variable the script needs
    Given the Docker Compose database service
    Then it mounts scripts/db_init and passes the application role settings

  Scenario: The script refuses to run without its credentials
    Given the init script
    When I run it with the application database password missing
    Then it stops with a message naming APP_DB_PASS

  Scenario: The script creates the application role and database in a real Postgres
    Given a throwaway Postgres server
    When I run the init script with an awkward password
    Then the application role can log in with that password
    And the application database exists and is owned by that role
    And a wrong password is rejected

  Scenario: The script also works when the image has already created the application database
    Given a throwaway Postgres server
    And the application database already exists, owned by the superuser
    When I run the init script with POSTGRES_DB set to that same database
    Then the application role can log in with that password
    And the application database exists and is owned by that role
