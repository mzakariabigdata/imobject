"""
Module test_orm.py - Test suite for the ORMCollection module.

This module contains unit tests for the ORM (Object-Relational Mapping) for ObjDict implementation.

Functions:

  describe_find_by(): Function to test the find_by() method of ORMCollection clas.
  describe_where(): Function to test the where() method of ORMCollection class.
  describe_group_by(): Function to test the group_by() method of ORMCollection class.
  describe_destinct(): Function to test the destinct() method of ORMCollection class.
  describe_all_offset_limit(): Function to test the all(), offset and limit of ORMCollection class.
  describe_order_by(): Function to test the order_by() method of ORMCollection class.

To run the tests, simply execute this module as a script, e.g., 
with the command `python -m pytest test_orm.py`.
The tests will be discovered and run automatically by the Pytest testing framework.

This module requires the following external libraries to be installed:
# - 
# - 

"""

import re
import pytest
from imobject import (
    OrmCollection,
    BaseMultipleFound,
    BaseNotFound,
    Query,
    Filter,
)


def describe_where():
    """Function to test the where() method of the ORMCollection class.

        This function uses the `pytest.mark.parametrize()` decorator to define a set of test cases
    that cover various use cases of the `where()` method.

    Each test case calls the `where()` method with a specific query and asserts that the returned
    results match the expected results.
    """

    # Paramétrisation des tests
    @pytest.mark.parametrize(
        "query, expected_names",
        [
            (
                Query([Filter("age", None, 30)]),
                {"Charlie", "Dave"},
            ),  # Test finding all elements with gender equal to male and age equal to 30 with Query
            (
                Query([Filter("age", None, 30)]) & Query([Filter("age", None, 30)]),
                {"Dave", "Charlie"},
            ),
            (
                Query([Filter("age", None, 30)])
                & Query([Filter("name", "startswith", "D")]),
                {"Dave"},
            ),
            (
                Query([Filter("age", None, 30)]) | Query([Filter("age", None, 40)]),
                {"Dave", "Bob", "Charlie"},
            ),
        ],
        # Ajout d'un label pour identifier clairement la paramétrisation dans les rapports de tests
        ids=["age=30", "age=30&age=30", "age=30&name=D*", "age=30|age=40"],
    )
    # Test pour vérifier que where() renvoie les résultats attendus
    def test_where_query_with_expected_results(
        my_orm_collection, query, expected_names
    ):
        # Appel à la méthode where() de l'ORM avec le query spécifié
        results = my_orm_collection.where(query)
        # Vérification de la longueur des résultats renvoyés
        assert len(results) == len(expected_names)
        # Vérification que les noms des résultats renvoyés sont bien ceux attendus
        result_names = set(result["name"] for result in results)
        assert result_names == expected_names

    @pytest.mark.parametrize(
        "query, expected_result",
        [
            pytest.param({"age__gt": "25"}, TypeError, id="type_error_age_gt_25"),
            pytest.param({"age__lt": "25"}, TypeError, id="type_error_age_lt_25"),
            pytest.param({"age__not": "25"}, TypeError, id="type_error_age_not_25"),
            pytest.param({"age__lte": "25"}, TypeError, id="type_error_age_lte_25"),
            pytest.param({"age__eq": "25"}, TypeError, id="type_error_age_eq_25"),
            pytest.param({"age__gte": "25"}, TypeError, id="type_error_age_gte_25"),
            pytest.param({"age__in": 25}, TypeError, id="type_error_age_in_25"),
            pytest.param(
                {"age__nin": 25}, TypeError, id="type_error_age_nin_25"
            ),  # Test TypeError
            pytest.param(
                {"age__contains": 25}, TypeError, id="type_error_age_contains_25"
            ),  # Test TypeError
            pytest.param(
                {"age__endswith": 25}, TypeError, id="type_error_age_endswith_25"
            ),  # Test TypeError
            pytest.param(
                {"age__startswith": 25}, TypeError, id="type_error_age_startswith_25"
            ),  # Test TypeError
            pytest.param(
                Query([Filter("age", "test_not_op", 30)]),
                ValueError,
                id="value_error_invalid_operator",
            ),  # Test not valid operator,
            pytest.param(
                {"name__notValid": "i"}, ValueError, id="value_error_invalid_parameter"
            ),  # Test not valid operator
        ],
    )
    def test_where_with_errors(my_orm_collection, query, expected_result):
        if expected_result == TypeError:
            with pytest.raises(TypeError):
                my_orm_collection.where(**query)
        elif expected_result == ValueError and isinstance(query, Query):
            with pytest.raises(expected_result):
                my_orm_collection.where(query)
        elif expected_result == ValueError:
            with pytest.raises(ValueError):
                my_orm_collection.where(**query)

    # Définition des paramètres d'entrée et des résultats attendus pour chaque test
    @pytest.mark.parametrize(
        "query, expected_names",
        [
            # Test pour trouver tous les éléments avec l'âge égal à 25
            pytest.param({"age": 25}, {"Alice"}, id="age=25"),
            # Test pour trouver tous les éléments avec le genre masculin et l'âge égal à 30
            pytest.param(
                {"gender": "male", "age": 30},
                {"Charlie", "Dave"},
                id="gender=male&age=30",
            ),
            # Test pour trouver tous les éléments avec le nom contenant la lettre "a"
            pytest.param({"name": ".*a.*"}, {"Charlie", "Dave"}, id="name_contains_a"),
            # Test pour trouver tous les éléments où l'âge est supérieur à 25 et le nom contient "v"
            pytest.param(
                {"age__gt": 25, "name__contains": "v"},
                {"Dave"},
                id="age>25&name_contains_v",
            ),
            pytest.param(
                {"age__in": [25, 30], "name__contains": "v"},
                {"Dave"},
                id="agein25,30&name_contains_v",
            ),
            pytest.param(
                {"age__lt": 40, "name__contains": "v"},
                {"Dave"},
                id="age=40&name_contains_v",
            ),
            pytest.param(
                {"age__not": 40, "name__contains": "v"},
                {"Dave"},
                id="age!=40&name_contains_v",
            ),
            pytest.param(
                {"age__eq": 40, "name__contains": "b"},
                {"Bob"},
                id="age==40&name_contains_b",
            ),
            pytest.param(
                {"age__lte": 30, "name__contains": "v"},
                {"Dave"},
                id="age<=30&name_contains_v",
            ),
            pytest.param(
                {"age__gte": 30, "name__contains": "v"},
                {"Dave"},
                id="age>=30&name_contains_v",
            ),
            pytest.param(
                {"age__nin": [25], "name__contains": "v"},
                {"Dave"},
                id="age!=25,&name_contains_v",
            ),
            pytest.param(
                {"age__nin": [25], "name__endswith": "e"},
                {"Dave", "Charlie"},
                id="age=40&name__endswith_v",
            ),
            # Test pour trouver tous les éléments avec le nom contenant la lettre "z"
            pytest.param(
                {"name": re.compile(r".*z.*", re.IGNORECASE)},
                set(),
                id="name_contains_z",
            ),
            # Test pour trouver tous les éléments avec le nom contenant la lettre "a" ou "e"
            pytest.param(
                {"name": ".*a.*|.*e.*"},
                {"Alice", "Charlie", "Dave"},
                id="name_contains_a_or_e",
            ),
            # Test pour trouver tous les éléments avec le nom se terminant par "ie"
            pytest.param(
                {"name": re.compile(r".*ie$", re.IGNORECASE)},
                {"Charlie"},
                id="name_ends_with_ie",
            ),
            # Test pour trouver tous les éléments avec un nom vide
            # (devrait renvoyer tous les éléments)
            pytest.param(
                {"name": ""}, {"Alice", "Bob", "Charlie", "Dave"}, id="name_empty"
            ),
            # Test  sans paramètres (devrait renvoyer 0 éléments)
            pytest.param({}, set(), id="no_params"),
            # Test pour trouver tous les éléments avec l'âge égal à 100
            # (devrait renvoyer un ensemble vide)
            pytest.param({"age": 100}, set(), id="age=100"),
            # Test pour trouver tous les éléments avec le nom commençant par "A"
            pytest.param({"name": "^A.*"}, {"Alice"}, id="name_starts_with_A"),
            # Test pour trouver tous les éléments avec le nom se terminant par "e"
            pytest.param(
                {"name": ".*e$"}, {"Alice", "Charlie", "Dave"}, id="name_ends_with_e"
            ),
            pytest.param(
                {"name": "^A.*|.*e$"},
                {"Alice", "Dave", "Charlie"},
                id="name_ends_with_e&name_starts_with_A",
            ),  # Test finding all elements with name starting with "A" or ending with "e"
        ],
    )
    def test_orm_collection_where(my_orm_collection, query, expected_names):
        # Test finding elements with the given query
        results = my_orm_collection.where(**query)
        assert len(results) == len(expected_names)
        assert {result["name"] for result in results} == set(expected_names)

        # Test that where function returns a new OrmCollection instance
        results = my_orm_collection.where(age=25)
        assert my_orm_collection != results


def describe_find_by():
    """Function to test the find_by() method of the ORMCollection class.

        This function uses the `pytest.mark.parametrize()` decorator to define a set of test cases
    that cover various use cases of the `find_by()` method.

    Each test case calls the `find_by()` method with a specific query and asserts that the returned
    results match the expected results.
    """

    @pytest.mark.parametrize(
        "query, expected_result",
        [
            pytest.param(
                {"name": ".*a.*"},
                BaseMultipleFound,
                id="find_multiple_elements_with_name_containing_a",
            ),
            pytest.param(
                {"age": 20},
                BaseNotFound,
                id="find_element_with_age_equal_to_20",
            ),
            pytest.param(
                {"name__contains": "v"},
                {"name": "Dave", "age": 30, "gender": "male"},
                id="find_element_with_name_containing_v",
            ),
        ],
    )
    def test_find_by(my_orm_collection, query, expected_result):
        if expected_result == BaseMultipleFound:
            with pytest.raises(BaseMultipleFound):
                my_orm_collection.find_by(**query)
        elif expected_result == BaseNotFound:
            with pytest.raises(BaseNotFound):
                my_orm_collection.find_by(**query)
        else:
            result = my_orm_collection.find_by(**query)
            assert result == expected_result


def describe_group_by():
    """Function to test the group_by() method of the ORMCollection class.

        This function uses the `pytest.mark.parametrize()` decorator to define a set of test cases
    that cover various use cases of the `group_by()` method.

    Each test case calls the `group_by()` method with a specific query and asserts that the returned
    results match the expected results.
    """

    @pytest.mark.parametrize(
        "group_func,expected_output",
        [
            pytest.param(
                lambda x: x["name"],
                {
                    "Alice": [
                        {"name": "Alice", "age": 25, "gender": "female", "taf": "psy"},
                        {
                            "name": "Alice",
                            "age": 80,
                            "gender": "male",
                            "taf": "retraite",
                        },
                    ],
                    "Bob": [{"name": "Bob", "age": 40, "gender": "male", "taf": "cia"}],
                    "Charlie": [
                        {"name": "Charlie", "age": 30, "gender": "male", "taf": "etud"},
                        {"name": "Charlie", "age": 30, "gender": "male", "taf": "prof"},
                    ],
                    "Dave": [
                        {"name": "Dave", "age": 30, "gender": "male", "taf": "ing"},
                        {"name": "Dave", "age": 31, "gender": "male", "taf": "chomor"},
                    ],
                },
                id="group_by_name",
            ),
            pytest.param(
                lambda x: x["gender"],
                {
                    "female": [
                        {"name": "Alice", "age": 25, "gender": "female", "taf": "psy"}
                    ],
                    "male": [
                        {
                            "name": "Alice",
                            "age": 80,
                            "gender": "male",
                            "taf": "retraite",
                        },
                        {"name": "Bob", "age": 40, "gender": "male", "taf": "cia"},
                        {"name": "Charlie", "age": 30, "gender": "male", "taf": "etud"},
                        {"name": "Charlie", "age": 30, "gender": "male", "taf": "prof"},
                        {"name": "Dave", "age": 30, "gender": "male", "taf": "ing"},
                        {"name": "Dave", "age": 31, "gender": "male", "taf": "chomor"},
                    ],
                },
                id="group_by_gender",
            ),
        ],
    )
    def test_orm_collection_group_by(
        my_orm_collection_group, group_func, expected_output
    ):
        """
        GIVEN a list of objects and a grouping function
        WHEN group_by() is called
        THEN the objects should be grouped according to the function
        """

        results = my_orm_collection_group.group_by(group_func)
        assert len(results) == len(expected_output)
        assert results == expected_output

    @pytest.mark.parametrize(
        "data, group_func, expected_output",
        [
            pytest.param(
                [1, 2, 3, 4],
                lambda x: x % 2 == 0,
                {True: [2, 4], False: [1, 3]},
                id="numbers",
            ),
            pytest.param(
                ["apple", "banana", "orange", "pear", "bouger"],
                lambda x: x[0],
                {
                    "a": ["apple"],
                    "b": ["banana", "bouger"],
                    "o": ["orange"],
                    "p": ["pear"],
                },
                id="fruits",
            ),
        ],
    )
    def test_simple_orm_collection_group_by(data, group_func, expected_output):
        lst_orm = OrmCollection(data)
        results = lst_orm.group_by(group_func)
        assert len(results) == len(expected_output)
        assert results == expected_output


def describe_order_by():
    """Function to test the order_by(() method of the ORMCollection class.

        This function uses the `pytest.mark.parametrize()` decorator to define a set of test cases
    that cover various use cases of the `order_by(()` method.

    Each test case calls the `order_by()` method with a specific query and asserts that the returned
    results match the expected results.
    """

    @pytest.mark.parametrize(
        "order_by_key, expected_output",
        [
            pytest.param(
                "age",
                [
                    {"name": "Alice", "age": 25, "gender": "female"},
                    {"name": "Charlie", "age": 30, "gender": "male"},
                    {"name": "Dave", "age": 30, "gender": "male"},
                    {"name": "Bob", "age": 40, "gender": "male"},
                ],
                id="order_by_age",
            ),
            pytest.param(
                lambda x: x["name"],
                [
                    {"name": "Alice", "age": 25, "gender": "female"},
                    {"name": "Bob", "age": 40, "gender": "male"},
                    {"name": "Charlie", "age": 30, "gender": "male"},
                    {"name": "Dave", "age": 30, "gender": "male"},
                ],
                id="order_by_name",
            ),
        ],
    )
    def test_order_by(my_orm_collection, order_by_key, expected_output):
        ordered_lst = my_orm_collection.order_by(order_by_key)
        assert ordered_lst == expected_output

    @pytest.mark.parametrize(
        "invalid_key_type, expected_error",
        [(123, TypeError), (None, ValueError)],
        ids=["invalid_key_type_type_error", "missing_key_func_value_error"],
    )
    def test_order_by_with_invalid_key_type(
        my_orm_collection, invalid_key_type, expected_error
    ):
        with pytest.raises(expected_error):
            my_orm_collection.order_by(invalid_key_type)

        lst = OrmCollection([4, 2, 1, "3"])
        with pytest.raises(expected_error):
            lst.order_by(invalid_key_type)

    @pytest.mark.parametrize(
        "data, expected_output",
        [
            pytest.param([4, 2, 1, 3], [1, 2, 3, 4], id="simple_list_of_integers"),
            pytest.param(
                ["apple", "banana", "orange", "f", "pear", "c'est encore moi"],
                ["f", "pear", "apple", "banana", "orange", "c'est encore moi"],
                id="list_of_strings",
            ),
        ],
    )
    def test_simple_order_by(data, expected_output):
        lst = OrmCollection(data)
        ordered_lst = lst.order_by()
        assert ordered_lst == expected_output

    @pytest.mark.parametrize(
        "data, key_func, expected_output",
        [
            ([4, 2, 1, 3], lambda x: -x, [4, 3, 2, 1]),
            (
                ["apple", "banana", "orange", "f", "pear", "c'est encore moi"],
                len,
                ["f", "pear", "apple", "banana", "orange", "c'est encore moi"],
            ),
        ],
        ids=["order_by_reversed", "order_by_len"],
    )
    def test_order_by_with_key_func(data, key_func, expected_output):
        lst = OrmCollection(data)
        ordered_lst = lst.order_by(key_func)
        assert ordered_lst == expected_output


def describe_all_offset_limit():
    """Function to test the all(), limit() and offset() methods of the ORMCollection class.

        This function uses the `pytest.mark.parametrize()` decorator to define a set of test cases
    that cover various use cases of the `all()`, `limit()` and `where()` methods.

    Each test case calls the `all()`, `limit()` and `where()` methodswith a specific query and
    asserts that the returned results match the expected results.
    """

    @pytest.mark.parametrize(
        "method, args, expected_output",
        [
            pytest.param(
                "all",
                [],
                [
                    {"name": "Alice", "age": 25, "gender": "female"},
                    {"name": "Bob", "age": 40, "gender": "male"},
                    {"name": "Charlie", "age": 30, "gender": "male"},
                    {"name": "Dave", "age": 30, "gender": "male"},
                ],
                id="test_all",
            ),
            pytest.param(
                "offset",
                [2],
                [
                    {"name": "Charlie", "age": 30, "gender": "male"},
                    {"name": "Dave", "age": 30, "gender": "male"},
                ],
                id="test_offset",
            ),
            pytest.param(
                "limit",
                [2],
                [
                    {"name": "Alice", "age": 25, "gender": "female"},
                    {"name": "Bob", "age": 40, "gender": "male"},
                ],
                id="test_limit",
            ),
        ],
    )
    def test_orm_collection_methods(my_orm_collection, method, args, expected_output):
        # [X] TODO: implement obj.to_dict()
        result = getattr(my_orm_collection, method)(*args)
        assert len(result) == len(expected_output)
        # for idx, obj in enumerate(result):
        #     assert obj.to_dict() == expected_output[idx]


def describe_destinct():
    """Function to test the destinct() method of the ORMCollection class.

        This function uses the `pytest.mark.parametrize()` decorator to define a set of test cases
    that cover various use cases of the `destinct()` method.

    Each test case calls the `destinct()` method with a specific query and asserts that the returned
    results match the expected results.
    """

    @pytest.mark.parametrize(
        "data, expected_output",
        [
            pytest.param([1, 2, 3, 4], [1, 2, 3, 4], id="distinct_with_no_duplicates"),
            pytest.param(
                [1, 2, 2, 3, 4, 4], [1, 2, 3, 4], id="distinct_with_duplicates"
            ),
            pytest.param(
                ["apple", "banana", "orange", "f", "pear", "orange"],
                ["apple", "banana", "orange", "f", "pear"],
                id="distinct_with_strings",
            ),
        ],
    )
    def test_orm_collection_distinct(data, expected_output):
        lst = OrmCollection(data)
        distinct_lst = lst.distinct()
        assert distinct_lst == expected_output

    @pytest.mark.parametrize(
        "fields, expected",
        [
            pytest.param(
                ("name", "age"),
                {
                    ("Alice", 25),
                    ("Alice", 80),
                    ("Dave", 30),
                    ("Dave", 31),
                    ("Bob", 40),
                    ("Charlie", 30),
                },
                id="distinct_two_fields",
            ),
        ],
    )
    def test_distinct(my_orm_collection_group, fields, expected):
        # Test with two fields
        distinct_coll = my_orm_collection_group.distinct(*fields)
        assert len(distinct_coll) == len(expected)
        assert {(person.name, person.age) for person in distinct_coll} == expected

        # Test with missing argument
        with pytest.raises(ValueError):
            my_orm_collection_group.distinct()
