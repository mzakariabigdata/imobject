# features/orm_collection.feature

Feature: OrmCollection Distinct

  Scenario: Distinct with no duplicates
    Given I have an OrmCollection with data "1,2,3,4"
    When I call the distinct method
    Then I expect the distinct list to be "1,2,3,4"

  Scenario: Distinct with duplicates
    Given I have an OrmCollection with data "1,2,2,3,4,4"
    When I call the distinct method
    Then I expect the distinct list to be "1,2,3,4"

  Scenario: Distinct with strings
    Given I have an OrmCollection with data "apple,banana,orange,f,pear,orange"
    When I call the distinct method
    Then I expect the distinct list to be "apple,banana,orange,f,pear"
