Feature: dependency basics
    As an ambitious project
    We will use dependency injection
    So that we are decoupled and can easily test and mock

    Scenario: With the original dependency
    Given a fixture providing the class
    When the dependency is instantiated
    Then dep_method returns 1000 * our value

    Scenario: With our mocked dependency
    Given a fixture providing the class
    When the dependency is instantiated
    Then dep_method returns 5000 * our value
