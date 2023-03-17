import json
from behave import given, when, then
from behave.runner import Context
from behave.model import Table
from typing import Dict
from imobject import ObjectFactory

class Parent:
    def __init__(self, name):
        self.name = name

    # def __repr__(self):
    #     return f"Parent(name={self.name}, child1={self.child1}, child2={self.child2})"


class Child:
    def __init__(self, age):
        self.age = age 

    def __repr__(self):
        return f"Child(age={self.age})"


@given("a class map with the following classes")
def step_given_class_map(context):
    context.class_map = {}
    for row in context.table:
        context.class_map[row["class_type"]] = globals()[row["class_name"]]
    print(context.class_map)

@given("a configuration for a Parent object")
def step_given_configuration_parent(context):
    context.configuration = {"class": "Parent", "params": {"name": "Parent1"}}

@given("a configuration for a Parent object with a single Child attribute")
def step_given_configuration_parent_single_child(context):
    row = context.table[0]
    context.configuration = {
        "class": row["parent_class"],
        "params": json.loads(row["parent_params"]),
        "child": {"class": row["child_class"], "params": json.loads(row["child_params"])}
    }
    print(context.configuration)

@when('I create an object using the object factory')
def step_when_create_object(context):
    factory = ObjectFactory(context.configuration , context.class_map)
    context.obj = factory.get_object()
    print(context.obj)

@then('the created object should be an instance of the Parent class')
def step_then_instance_of_parent(context):
    assert isinstance(context.obj, context.class_map['Parent'])

@then('the child property should be an instance of the Child class')
def step_then_child_instance_of_child(context):
    assert isinstance(context.obj.child, context.class_map['Child'])

@then("the created object should be an instance of the Parent class with a single Child attribute")
def step_then_created_object_instance_of_parent_single_child(context):
    assert isinstance(context.obj, Parent)
    assert isinstance(context.obj.child, Child)

@then("the created object should be an instance of the Parent class with multiple Children attributes")
def step_then_created_object_instance_of_parent_multiple_children(context):
    assert isinstance(context.obj, Parent)
    assert len(context.obj.children) == 2
    for child in context.obj.children:
        assert isinstance(child, Child)

@given("a configuration for a Parent object with multiple Children attributes")
def step_given_configuration_parent_multiple_children(context):
    row = context.table[0]
    context.configuration = {
        "class": row["parent_class"],
        "params": json.loads(row["parent_params"]),
        "children": [
            {"class": row["child1_class"], "params": json.loads(row["child1_params"])},
            {"class": row["child2_class"], "params": json.loads(row["child2_params"])}
        ]
    }