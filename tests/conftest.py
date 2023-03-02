"""The conftest module contains fixtures and configuration for pytest.

Fixtures:
    - my_orm_collection: Fixture that returns an instance of the OrmCollection class with test data.
    - my_orm_collection_group: Fixture that returns an ORM collection of objects representing 
                                people, with additional data on their occupation.
    - sample_obj_dict: Fixture that returns a sample ObjDict object.
    - person_class: Fixture that returns a sample Person object class.
    - person: Fixture that returns a sample Person object.
    - obj: Fixture that returns a sample ObjDict object with nested Person object.

Classes:
    - Person: Sample class representing a person with a name and an age.

Returns:
    This module does not return anything.
"""
import pytest
from _pytest.runner import runtestprotocol
from imobject import (
    OrmCollection,
    ObjDict,
)


def generate_examples(item, report):
    """
    Generate examples for each test.

    Parameters:
    - item: The test item.
    - report: The test report.

    Returns:
    - None
    """
    if report.when == "call":
        # Récupérer le nom de la fonction de test
        # func_name = item.name.split("[")[0]
        # Récupérer les noms des paramètres
        argnames = item.fixturenames
        # Récupérer les valeurs des paramètres
        try:
            argvalues = item.callspec.params.values()
            print(argnames, argvalues)
            # test_first ['lst', 'args', 'expected_output'] dict_values([[1, 2, 3], (2,), [1, 2]])
        except ValueError:
            pass


def pytest_runtest_protocol(item, nextitem):
    """
    Edit each test before running.

    Parameters:
    - item: The test item.
    - nextitem: The next test item.

    Returns:
    - bool: True if the tests were run successfully, otherwise False.
    """
    reports = runtestprotocol(item, nextitem=nextitem)
    for report in reports:
        generate_examples(item, report)
    return True


@pytest.fixture
def my_orm_collection():
    """Fixture that returns an instance of the OrmCollection class with test data.

    Returns an instance of the OrmCollection class containing four dictionaries created with
    the class ObjDict, each representing a person with a name (key "name"), an age (key "age")
    and a sex ("gender" key).

    Returns:
        OrmCollection: an instance of the OrmCollection class.
            - 'name': str, the name of the person.
            - 'age': int, the age of the person.
            - 'gender': str, the gender of the person.
    """
    return OrmCollection(
        [
            ObjDict({"name": "Alice", "age": 25, "gender": "female"}),
            ObjDict({"name": "Bob", "age": 40, "gender": "male"}),
            ObjDict({"name": "Charlie", "age": 30, "gender": "male"}),
            ObjDict({"name": "Dave", "age": 30, "gender": "male"}),
        ]
    )


@pytest.fixture
def my_orm_collection_group():
    """
    A fixture that returns an ORM collection of objects representing people, with additional data
    on their occupation.

    Returns an instance of the OrmCollection class containing four dictionaries created with
    the class ObjDict, each representing a person with a name (key "name"), an age (key "age"),
    a sex ("gender" key) and occupation ("taf" key)

    Returns:
        OrmCollection: A collection of ObjDict objects, where each object has the following fields:
            - 'name': str, the name of the person.
            - 'age': int, the age of the person.
            - 'gender': str, the gender of the person.
            - 'taf': str, the occupation of the person.
    """
    return OrmCollection(
        [
            ObjDict({"name": "Alice", "age": 25, "gender": "female", "taf": "psy"}),
            ObjDict({"name": "Alice", "age": 80, "gender": "male", "taf": "retraite"}),
            ObjDict({"name": "Bob", "age": 40, "gender": "male", "taf": "cia"}),
            ObjDict({"name": "Charlie", "age": 30, "gender": "male", "taf": "etud"}),
            ObjDict({"name": "Charlie", "age": 30, "gender": "male", "taf": "prof"}),
            ObjDict({"name": "Dave", "age": 30, "gender": "male", "taf": "ing"}),
            ObjDict({"name": "Dave", "age": 31, "gender": "male", "taf": "chomor"}),
        ]
    )


@pytest.fixture
def sample_obj_dict():
    """Fixture that returns a sample ObjDict object."""

    return ObjDict(
        {
            "name": "John",
            "age": 30,
            "address": {"street": "123 Main St", "city": "Anytown", "state": "CA"},
            "scores": [90, 80, 95],
        }
    )


@pytest.fixture(scope="module")
def person_class():
    """Fixture that returns a sample Person object."""

    class Person:
        """
        A class representing a person with a name, age, and salary.

        Attributes:
        - name (str): The name of the person.
        - age (int): The age of the person.
        - salary (float): The salary of the person.

        Methods:
        - ret_name(): Returns the name of the person (as a property).
        - get_name(): Returns the name of the person.
        - upper_name(): Returns the name of the person in uppercase letters.
        - get_age(): Returns the age of the person.
        - change_name(new_name: str): Changes the name of the person to a new name.
        - change_age(new_age: int): Changes the age of the person to a new age.
        - is_adult(): Returns True if the person is an adult (18 or older), otherwise False.
        - set_name(new_name: str): Changes the name of the person to a new name.
        - __repr__(): Returns a string representation of the person in the format
                    "Person(name='[name]', age=[age], salary=[salary])".
        """

        def __init__(self, name: str, age: int, salary: float):
            """
            Initializes a Person object with a name, age, and salary.

            Parameters:
            - name (str): The name of the person.
            - age (int): The age of the person.
            - salary (float): The salary of the person.
            """
            self.name = name
            self.age = age
            self.salary = salary

        @property
        def ret_name(self) -> str:
            """
            Returns the name of the person.

            Returns:
            - (str): The name of the person.
            """
            return self.name

        def get_name(self) -> str:
            """
            Returns the name of the person.

            Returns:
            - (str): The name of the person.
            """
            return self.name

        def upper_name(self) -> str:
            """
            Returns the name of the person in uppercase letters.

            Returns:
            - (str): The name of the person in uppercase letters.
            """
            return self.name.upper()

        def get_age(self) -> int:
            """
            Returns the age of the person.

            Returns:
            - (int): The age of the person.
            """
            return self.age

        def change_name(self, new_name: str) -> None:
            """
            Changes the name of the person to a new name.

            Parameters:
            - new_name (str): The new name for the person.
            """
            self.name = new_name

        def change_age(self, new_age: int) -> None:
            """
            Changes the age of the person to a new age.

            Parameters:
            - new_age (int): The new age for the person.
            """
            self.age = new_age

        def is_adult(self) -> bool:
            """
            Returns True if the person is an adult (18 or older), otherwise False.

            Returns:
            - (bool): True if the person is an adult, otherwise False.
            """
            return self.age >= 18

        def set_name(self, new_name: str) -> None:
            """
            Changes the name of the person to a new name.

            Parameters:
            - new_name (str): The new name for the person.
            """
            self.name = new_name

        def __repr__(self) -> str:
            """
            Returns a string representation of the person in the format
                "Person(name='[name]', age=[age], salary=[salary])".
            Parameters:
            - (str): string representation of the person.
            """
            return f"Person(name='{self.name}', age={self.age}, age={self.salary} )"

    return Person


@pytest.fixture
def person():
    """Fixture that returns a sample Person object."""

    class Person:  # pylint: disable=too-few-public-methods

        """
        A class representing a person.

        Attributes:
        -----------
        name: str
            The name of the person.
        age: int
            The age of the person.

        Methods:
        --------
        __repr__() -> str:
            Return a string representation of the person.
        """

        def __init__(self, name: str, age: int) -> None:
            """
            Initializes a Person object with the specified name and age.

            Parameters:
            ----------
            name: str
                The name of the person.
            age: int
                The age of the person.
            """
            self.name = name
            self.age = age

        def __repr__(self) -> str:
            """
            Returns a string representation of the person.

            Returns:
            --------
            str:
                A string representation of the person.
            """
            return f"Person(name='{self.name}', age={self.age})"

    return Person("zakaria", 33)


@pytest.fixture
def obj(person):  # pylint: disable=redefined-outer-name
    """Fixture that returns a sample ObjDict object with nested Person object."""

    return ObjDict({"a": 1, "test": {"zak": person}, "b": {"c": 2, "d": [3, 4]}})
