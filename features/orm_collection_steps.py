# features/steps/orm_collection_steps.py

from behave import *
from imobject.orm_collection import OrmCollection

use_step_matcher("parse")


@given("I have an OrmCollection with data {data}")
def step_impl(context, data):
    context.collection = OrmCollection(data.split(","))


@when("I call the distinct method")
def step_impl(context):
    context.distinct_list = context.collection.distinct()


@then("I expect the distinct list to be {expected}")
def step_impl(context, expected):
    expected_list = expected.split(",")
    for item in expected_list:
        assert item in context.distinct_list


@when("I call the where method with a query {query}")
def step_impl(context, query):
    query = query.replace("'", '"')
    context.results = context.collection.where(query)


@then("I expect to get the results {expected}")
def step_impl(context, expected):
    expected_list = expected.split(",")
    for item in expected_list:
        assert item in [result["name"] for result in context.results]
