Feature: Publishing as an example
  Site where you can publish your articles.

  Scenario: Publishing articles
    Given JimmyJimmy
    And I have an article
    When I update the new article with just a name
    And I publish with name and author information
    Then I can see there are two articles published