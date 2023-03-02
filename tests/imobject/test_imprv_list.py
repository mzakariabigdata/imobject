"""Module test_improv_list.py - Test suite for the ImprovedList module.

This module contains unit tests for the ImprovedList implementation.

Functions:

  describe_inspect(): Function to test inspect() function for ImprovedList class.
  describe_last(): Function to test last() function for ImprovedList class.
  describe_map(): Function to test map() function for ImprovedList class.
  describe_fisrt(): Function to test fisrt() function for ImprovedList class.

  To run the tests, simply execute this module as a script, e.g., 
with the command `python -m pytest test_improv_list.py`.
The tests will be discovered and run automatically by the Pytest testing framework.

This module requires the following external libraries to be installed:
-
"""
import sys
from datetime import datetime
from io import StringIO
import pytest
from imobject import ImprovedList


def describe_inspect():
    """Describe inspect() function of ImprovedList"""

    @pytest.mark.parametrize(
        "lst, expected_output",
        [
            pytest.param([], "[]\n", id="empty_list"),
            pytest.param([1], "ImprovedList(int) data:\n1\n", id="int_list"),
            pytest.param(
                [1, "string", [1, 2], {"a": 1, "b": 2}],
                "ImprovedList(int) data:\n1\n'string'\n[1, 2]\n{'a': 1, 'b': 2}\n",
                id="simple_list",
            ),
            pytest.param(
                [1, "string", [1, 2], {"a": 1, "b": {"z": 1, "m": [1, 2]}}],
                "ImprovedList(int) data:\n1\n'string'\n[1, 2]\n{'a': 1, 'b': {'m': [1, 2], 'z': 1}}\n",  # pylint: disable=line-too-long
                id="complex_list",
            ),
        ],
    )
    def test_inspect(lst, expected_output, capsys):
        # Test display of an ImprovedList object
        lst = ImprovedList(lst)
        lst.inspect  # pylint: disable=pointless-statement
        captured = capsys.readouterr()
        assert captured.out == expected_output
        assert captured.err == ""

    def test_inspect_obj():  # pylint: disable=unused-variable
        # Test that inspect method is called on element with inspect method defined
        class Inspectable:
            """Inspectable class for test"""

            def __init__(self, name):
                self.name = name

            def inspect(self):
                """inspect function"""
                print(f"Inspectable({self.name})")

            def set_name(self, new_name):
                """set name function"""
                self.name = new_name

        inspectable_list = ImprovedList(
            [Inspectable("element1"), Inspectable("element2")]
        )
        captured_output = StringIO()  # créer un StringIO pour capturer la sortie
        sys.stdout = captured_output  # rediriger la sortie standard vers StringIO
        inspectable_list.inspect  # appeler la méthode inspect() sur la liste # pylint: disable=pointless-statement
        sys.stdout = (
            sys.__stdout__
        )  # remettre la sortie standard à sa valeur par défaut
        assert (
            captured_output.getvalue()
            == "ImprovedList(Inspectable) data:\nInspectable(element1)\nInspectable(element2)\n"
        )  # la chaîne de caractères attendue pour la sortie de la méthode


def describe_fist():
    """Describe fist() function of ImprovedList"""

    @pytest.mark.parametrize(
        "lst, args, expected_output",
        [
            pytest.param([1, 2, 3], (), 1, id="test_first_simple_list"),
            pytest.param(
                [1, 2, 3], (2,), ImprovedList([1, 2]), id="test_first_two_elements"
            ),
            pytest.param([], (), None, id="test_first_empty_list"),
        ],
    )
    def test_first(lst, args, expected_output):
        """Test first() function of ImprovedList

        Args:
            lst (list): list of data
            args (int): n fist element
            expected_output (any): return any obj
        """
        # Test getting the first element of a list
        simple_list = ImprovedList(lst)
        assert simple_list.first(*args) == expected_output


def describe_last():
    """Descripe last() function of ImprovedList"""

    @pytest.mark.parametrize(
        "lst, arg, expected_output",
        [
            pytest.param([1, 2, 3], (), 3, id="last_element"),
            pytest.param([1, 2, 3], (2,), ImprovedList([2, 3]), id="last_two_elements"),
            pytest.param([], (), None, id="empty_list"),
        ],
    )
    def test_last(lst, arg, expected_output):
        # Test getting the last element of a list
        simple_list = ImprovedList(lst)
        assert simple_list.last(*arg) == expected_output


def describe_map():  # pylint: disable=too-many-statements
    """Descripe map() function of ImprovedList"""

    @pytest.mark.parametrize(
        "lst, attribute, expected_output",
        [
            pytest.param(
                [1, 2, 3],
                ":__str__",
                ["1", "2", "3"],
                id="string_representation",
            ),
            pytest.param(
                [1, 2, 3],
                str,
                ["1", "2", "3"],
                id="string_rep",
            ),
            pytest.param(
                [1, 2, 3], ":to_bytes", [b"\x01", b"\x02", b"\x03"], id="map_to_bytes"
            ),
            pytest.param([1, 2, 3], float, [1.0, 2.0, 3.0], id="real_part"),
            pytest.param([], ":__str__", [], id="empty_list"),
            (
                [1, 2, 3],
                lambda x: x * 2,
                [2, 4, 6],
            ),
            pytest.param([1, 2, 3, 4, 5], lambda x: x**2, [1, 4, 9, 16, 25]),
        ],
    )
    def test_map(lst, attribute, expected_output):
        # Test calling a method or attribute on each element of a list
        simple_list = ImprovedList(lst)
        assert simple_list.map(attribute) == ImprovedList(expected_output)

        # Test with called argument None
        with pytest.raises(ValueError, match="called cannot be None"):
            simple_list.map(None)

        with pytest.raises(
            TypeError,
            match="called must be a string start with ':' for obj method or '.' obj attribute, "
            "or a callable",
        ):
            simple_list.map(1)

        with pytest.raises(
            TypeError,
            match="called must be a string start with ':' for obj method or '.' obj attribute, "
            "or a callable",
        ):
            simple_list.map("test error")

    @pytest.mark.parametrize(
        "fucntion, expected_name_upper",
        [
            pytest.param(
                ":upper_name", ["ALICE", "BOB", "CHARLIE"], id="map_upper_name"
            ),
            pytest.param(":is_adult", [True, False, True], id="map_is_adult"),
            pytest.param(":get_age", [25, 12, 35], id="map_get_age"),
        ],
    )
    def test_map_person(person_class, fucntion, expected_name_upper):
        # Test calling a method on each element of a list of Person objects
        people = [
            person_class("Alice", 25, 100),
            person_class("Bob", 12, 364),
            person_class("Charlie", 35, 740),
        ]
        person_list = ImprovedList(people)
        assert person_list.map(fucntion) == ImprovedList(expected_name_upper)

    def test_map_with_args_and_kwargs(person_class):  # pylint: disable=unused-variable
        # create an ImprovedList with some objects
        lst = ImprovedList(
            [
                person_class("Alice", 25, 100),
                person_class("Bob", 30, 364),
                person_class("Charlie", 35, 740),
            ]
        )

        # define a function that takes two positional arguments and one keyword argument
        def add_age_and_salary(person, age_offset, salary=50000):
            person.age += age_offset
            person.salary += salary
            return person

        # apply the function to each object in the ImprovedList using map with arguments and kwargs
        result = lst.map(add_age_and_salary, age_offset=5, salary=60000)

        # check that the result is an ImprovedList
        assert isinstance(result, ImprovedList)

        # check that each object in the result has the expected age and salary values
        assert result[0].age == 30
        assert result[0].salary == 60100
        assert result[1].age == 35
        assert result[1].salary == 60364
        assert result[2].age == 40
        assert result[2].salary == 60740

    @pytest.mark.parametrize(
        "methode_obj, new_attribut, attribut, expected_names",
        [
            (
                ":change_name",
                {"new_name": "David"},
                "name",
                ["David", "David", "David"],
            ),
            (
                ":change_name",
                {"new_name": "Michael"},
                "name",
                ["Michael", "Michael", "Michael"],
            ),
            (":change_name", {"new_name": ""}, "name", ["", "", ""]),
            (
                ":change_age",
                {"new_age": 50},
                "age",
                [50, 50, 50],
            ),
            # Appeler la méthode "change_age" pour chaque objet en utilisant ":",
            # ce qui équivaut à appeler "obj.change_age("new_age" = 50)"
        ],
    )
    def test_map_method_obj(
        person_class, methode_obj, new_attribut, attribut, expected_names
    ):
        people = ImprovedList(
            [
                person_class("Alice", 25, 100),
                person_class("Bob", 30, 364),
                person_class("Charlie", 35, 740),
            ]
        )
        # Appeler la méthode avec des arguments et des kwargs sur chaque objet de la liste
        people.map(methode_obj, **new_attribut)
        assert [getattr(person, attribut) for person in people] == expected_names

    @pytest.mark.parametrize(
        "attribut_obj, attribut, expected_names",
        [
            (".name", "name", ["Alice", "Bob", "Charlie"]),
            (".age", "age", [25, 30, 35]),
        ],
    )
    def test_map_attrbut_obj(person_class, attribut_obj, attribut, expected_names):
        people = ImprovedList(
            [
                person_class("Alice", 25, 100),
                person_class("Bob", 30, 364),
                person_class("Charlie", 35, 740),
            ]
        )
        # Appeler la méthode avec des arguments et des kwargs sur chaque objet de la liste
        people.map(attribut_obj)
        assert [getattr(person, attribut) for person in people] == expected_names

    @pytest.mark.parametrize(
        "called, filter_func, expected_output",
        [
            (
                lambda x: x**2,
                lambda x: isinstance(x, int) and x % 2 == 0,
                [4, 4, 16, 36, 64, 100],
            ),
            (
                lambda x: x.upper(),
                lambda x: isinstance(x, str) and len(x) > 5,
                ["BANANA", "ORANGE", "STRAWBERRY", "WATERMELON"],
            ),
            (
                lambda x: x.capitalize(),
                lambda x: isinstance(x, str) and "a" in x.lower(),
                ["Apple", "Banana", "Orange", "Strawberry", "Grape", "Watermelon"],
            ),
            (
                lambda x: x * 2,
                lambda x: isinstance(x, int),
                ImprovedList([2, 4, 6, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]),
            ),
            (
                str,
                lambda x: isinstance(x, int) and x >= 3,
                ImprovedList(["3", "3", "4", "5", "6", "7", "8", "9", "10"]),
            ),
        ],
    )
    def test_filter_map_no_person_filter(
        person_class, called, filter_func, expected_output
    ):
        people = ImprovedList(
            [
                person_class("Alice", 25, 100),
                person_class("Bob", 30, 364),
                person_class("Charlie", 35, 740),
                1,
                2,
                3,
                "four",
                5.0,
                {"six": 6},
                [7],
                "Apple",
                "Banana",
                "Orange",
                "Strawberry",
                "Grape",
                "Watermelon",
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
            ]
        )
        result = people.map(called, filter_func=filter_func)
        assert result == expected_output

    def test_filter_map_person_filter(person_class):  # pylint: disable=unused-variable
        people = ImprovedList(
            [
                person_class("Alice", 25, 100),
                person_class("Bob", 30, 364),
                person_class("Charlie", 35, 740),
                1,
                2,
                3,
                "four",
                5.0,
                {"six": 6},
                [7],
                "Apple",
                "Banana",
                "Orange",
                "Strawberry",
                "Grape",
                "Watermelon",
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
            ]
        )

        result = people.map(
            lambda x: x.get_name(),
            filter_func=lambda x: isinstance(x, person_class) and x.age >= 30,
        )
        assert result == ImprovedList(["Bob", "Charlie"])

        result = people.map(
            ":get_name",
            filter_func=lambda x: isinstance(x, person_class) and x.age >= 30,
        )
        assert result == ImprovedList(["Bob", "Charlie"])

        result = people.map(
            ".name", filter_func=lambda x: isinstance(x, person_class) and x.age >= 30
        )
        assert result == ImprovedList(["Bob", "Charlie"])

        with pytest.raises(TypeError, match="ret_name is not callable"):
            people.map(
                ":ret_name",
                filter_func=lambda x: isinstance(x, person_class) and x.age >= 30,
            )

        with pytest.raises(
            AttributeError, match="Person object has no attribute 'not_exist_attribut'"
        ):
            people.map(".not_exist_attribut")

    def test_filter_map_filter():  # pylint: disable=unused-variable
        # Création d'une liste de dictionnaires représentant des étudiants
        students = ImprovedList(
            [
                {"name": "Alice", "grades": [8, 9, 7]},
                {"name": "Bob", "grades": [6, 7, 5]},
                {"name": "Charlie", "grades": [9, 9, 10]},
            ]
        )

        # Définition d'une fonction qui retourne la moyenne des notes d'un étudiant
        def average_grades(student, **kwargs):
            if "weights" in kwargs:
                weights = kwargs["weights"]
                if len(weights) != len(student["grades"]):
                    raise ValueError(
                        "Weights list must have the same length as grades list"
                    )
                grades = [
                    grade * weight for grade, weight in zip(student["grades"], weights)
                ]
                return sum(grades) / sum(weights)

            return sum(student["grades"]) / len(student["grades"])

        # Application de la fonction average_grades aux étudiants
        # ayant une note moyenne supérieure à 8
        top_students = students.filter(
            lambda s: average_grades(s, weights=[3, 1, 1]) > 8
        )
        assert top_students == [{"name": "Charlie", "grades": [9, 9, 10]}]

    def test_map_return_type():  # pylint: disable=unused-variable
        my_improved_list = ImprovedList(["hello", "world"])
        uppered_list = my_improved_list.map(":upper", return_type="list")
        assert uppered_list == ["HELLO", "WORLD"]

        with pytest.raises(
            ValueError, match="return_type must be 'ImprovedList' or 'list'"
        ):
            my_improved_list.map(":upper", return_type=list)

    def test_map_max_elements():  # pylint: disable=unused-variable
        my_list = ImprovedList([1, 2, 3, 4, 5])
        result = my_list.map(lambda x: x**2, max_elements=3)
        assert result == [1, 4, 9]

    def test_map_reversed():  # pylint: disable=unused-variable
        # Création d'une ImprovedList
        my_list = ImprovedList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        # Utilisation de map avec max_elements et reverse_order
        result = my_list.map(lambda x: x * 2, reverse_order=True)
        assert result == [20, 18, 16, 14, 12, 10, 8, 6, 4, 2]

    def test_map_max_elements_reversed():  # pylint: disable=unused-variable
        my_list = ImprovedList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        result = my_list.map(lambda x: x**2, max_elements=3, reverse_order=True)
        assert result == [9, 4, 1]

    def test_map_sort():  # pylint: disable=unused-variable
        class MyClass:  # pylint: disable=too-few-public-methods
            """class for test"""

            def __init__(self, name: str, date: str):
                self.name = name
                self.date = datetime.strptime(date, "%Y-%m-%d")

        # Créer une liste d'objets MyClass non triée
        objects = ImprovedList(
            [
                MyClass("Obj1", "2022-01-05"),
                MyClass("Obj2", "2022-02-03"),
                MyClass("Obj3", "2021-12-25"),
                MyClass("Obj4", "2022-01-20"),
            ]
        )

        # Définir une fonction pour trier les objets MyClass par date
        def sort_by_date(obj: MyClass) -> datetime:
            return obj.date

        # Utiliser la méthode map avec la fonction de tri pour obtenir une
        # liste triée des noms d'objets MyClass
        sorted_names = objects.map(called=lambda obj: obj.name, sort_func=sort_by_date)
        assert sorted_names == ["Obj3", "Obj1", "Obj4", "Obj2"]
