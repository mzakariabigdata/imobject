# features/orm_collection.feature

Feature: OrmCollection Where

  Scenario: Where with age=30
    Given I have an OrmCollection with data "Alice,25,F;Bob,40,M;Charlie,30,M;Dave,31,M;Dave,30,M;Alice,80,F"
    When I call the where method with a query {"age":30}
    Then I expect to get the results "Charlie,Dave"

  Scenario: Where with age=30 and name starts with D
    Given I have an OrmCollection with data "Alice,25,F;Bob,40,M;Charlie,30,M;Dave,31,M;Dave,30,M;Alice,80,F"
    When I call the where method with a query {"age":30, "name":"startswith(\"D\")"}
    Then I expect to get the results "Dave"

  Scenario: Where with age=30 or age=40
    Given I have an OrmCollection with data "Alice,25,F;Bob,40,M;Charlie,30,M;Dave,31,M;Dave,30,M;Alice,80,F"
    When I call the where method with a query {"$or":[{"age":30}, {"age":40}]}
    Then I expect to get the results "Dave,Bob
