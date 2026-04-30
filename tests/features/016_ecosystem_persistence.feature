Feature: Ecosystem persistence and testability
  As a CondorGP developer
  I want ecosystem state to persist in a predictable way
  So that runs are reproducible, sortable, and easy to test

  Background:
    Given an ecosystem repository configured with a writable root path

  Scenario: Time-prefixed run_id sorts naturally
    When a new ecosystem run_id is generated
    Then the run_id starts with date-time digits in "YYYYMMDDHHMMSS" format
    And the run_id can be sorted lexicographically for chronological ordering

  Scenario: Save append-only snapshots for one run_id
    Given an ecosystem with ecosystem_id "eco-demo" and run_id "20260429101530-demo"
    When the ecosystem is saved three times
    Then three versions exist for run_id "20260429101530-demo"
    And loading without a version returns the latest snapshot
    And loading a specific version returns that exact snapshot

  Scenario: One ecosystem can have multiple run_id values
    Given one ecosystem with generated ecosystem_id
    When one snapshot is saved for each of three different run_id values
    Then all three snapshots have different run_id values
    And all three snapshots share the same ecosystem_id

  Scenario: Parquet is used as phase 1 persistence
    Given a Parquet ecosystem repository
    When ecosystem state is persisted
    Then cells are written as Parquet records
    And ecosystem run metadata is written as Parquet records
    And a Parquet record with ecosystem run metadata within it is saved
    And persisted files are saved under "tests/test_data/ecosystem"
    And no Postgres dependency is required in phase 1

  Scenario: Ecosystem logic is decoupled from storage implementation
    Given an ecosystem constructed with an injected repository
    When the same ecosystem behavior is executed with an in-memory repository and a Parquet repository
    Then business behavior is consistent across both repositories

  # Phase 2 placeholders (intentional, not phase 1 acceptance)
  Scenario: Iceberg repository can be introduced without changing ecosystem logic
    Given a future Iceberg ecosystem repository implementing the same repository interface
    When repository wiring is switched from Parquet to Iceberg
    Then ecosystem domain behavior remains unchanged

  Scenario: Postgres repository can be introduced without changing ecosystem logic
    Given a future Postgres ecosystem repository implementing the same repository interface
    When repository wiring is switched from Parquet to Postgres
    Then ecosystem domain behavior remains unchanged
