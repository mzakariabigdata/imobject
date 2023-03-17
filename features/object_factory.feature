Feature: Object factory

    Scenario: Create a simple object
        Given a class map with the following classes
            | class_type | class_name |
            | Parent     | Parent     |
            | Child      | Child      |
        And a configuration for a Parent object
            | class  | params |
            | Parent | {}     |
        When I create an object using the object factory
        Then the created object should be an instance of the Parent class

    Scenario: Create a Parent object with a single Child attribute
        Given a class map with the following classes
            | class_type | class_name |
            | Parent     | Parent     |
            | Child      | Child      |
        And a configuration for a Parent object with a single Child attribute
            | parent_class | parent_params | child_class | child_params |
            | Parent       | {"name": "Parent1"} | Child      | {"age": 5}   |
        When I create an object using the object factory
        Then the created object should be an instance of the Parent class with a single Child attribute

    Scenario: Create a Parent object with multiple Children attributes
        Given a class map with the following classes
            | class_type | class_name |
            | Parent     | Parent     |
            | Child      | Child      |
        And a configuration for a Parent object with multiple Children attributes
            | parent_class | parent_params | child1_class | child1_params | child2_class | child2_params |
            | Parent       | {"name": "Parent1"} | Child      | {"age": 6}   | Child      | {"age": 7}   |
        When I create an object using the object factory
        Then the created object should be an instance of the Parent class with multiple Children attributes