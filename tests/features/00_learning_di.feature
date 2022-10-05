Feature: dependency basics
    As an ambitious project
    We will use dependency injection
    So that we are decoupled and can easily test and mock

    Scenario: With the original dependency
    Given a fixture providing the class
    When the dependency is instantiated
    Then dep_multiply returns 1000 * our value
    Then dep_add returns our value + 1000

    Scenario: With our mocked dependency
    Given a fixture providing the mocked class
    When the mocked dependency is instantiated
    Then dep_multiply mock returns 5000 * our value
    Then dep_add mock returns our value + 5000
