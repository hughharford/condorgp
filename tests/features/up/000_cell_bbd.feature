Feature: condorGP cells basics
    As an ambitious developer
    I need to be sure that BDD is at the core of how we work
    So that we can be sure of our foundations

    Scenario: Cell creation
      Given pre-created cells
      When another cell is created
      Then the celllist is incremented

    Scenario: Cell id
      Given a pre-created cell
      When the cell id is changed
      Then the new cell id is as expected
