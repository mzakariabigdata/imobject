"""
Module test_obj_dict.py - Test suite for the ObjDict module.

This module contains unit tests for the ObjDict implementation.

Functions:

  describe_objdict(): Function to test all functions for ObjDict class.

To run the tests, simply execute this module as a script, e.g., 
with the command `python -m pytest test_orm.py`.
The tests will be discovered and run automatically by the Pytest testing framework.

This module requires the following external libraries to be installed:
# - 
# - 

"""
import pytest
from imobject import ObjDict
from imobject import ImprovedList


def describe_objdict():
    """Function to test all functions for ObjDict class."""

    @pytest.mark.parametrize(
        "select_keys, expected",
        [
            (["c"], pytest.raises(KeyError)),
            (["b", "c", "d"], pytest.raises(KeyError)),
            (None, pytest.raises(TypeError)),
            ("b", pytest.raises(TypeError)),
            (["b", 1], pytest.raises(TypeError)),
        ],
        ids=[
            "Test with non-existent key in select",
            "Test with non-existent key in nested select",
            "Test with None argument for select",
            "Test with non-list argument for select",
            "Test with non-string element in select",
        ],
    )
    def test_obj_with_errors(
        obj, select_keys, expected
    ):  # pylint: disable=unused-variable
        """Test ObjDict.select() method with various error cases.

        Copy code
            Args:
            - obj: An ObjDict object.
            - select_keys: A list of keys or nested keys to select.
            - expected: An expected error type.

            Raises:
            - KeyError: If a non-existent key is provided in the select_keys argument.
            - TypeError: If the select_keys argument is not a list or if a non-string element is
                            provided in the list.
        """
        with expected:
            obj.select(select_keys)

    @pytest.mark.parametrize(
        "select_keys, expected",
        [
            pytest.param(["b"], {"b": {"c": 2, "d": [3, 4]}}, id="select_existing_key"),
            pytest.param([], {}, id="select_empty_list"),
        ],
    )
    def test_obj_dict(obj, select_keys, expected):  # pylint: disable=unused-variable
        """Test various methods of ObjDict.

        Args:
        - obj: An ObjDict object.
        - select_keys: A list of keys or nested keys to select.
        - expected: An expected dictionary object.

        Returns: None
        """

        # initialisation avec un dictionnaire
        # vérifier que l'objet initialisé est bien une instance de ObjDict
        assert isinstance(obj, ObjDict)

        obj.account = {}
        obj.account.unsername = "John"
        obj.account.password = "1234"
        obj.account.users = []
        obj.account.users.append({"name": "John", "age": 25})

        assert isinstance(obj.account.users, ImprovedList)
        # accès aux éléments avec la notation par point
        # obj.a == 1
        # obj.test.zak.age == 33
        # obj.test.zak.name == "zakaria"
        assert obj.b.c == 2
        # obj.b.d == [3, 4]
        # obj.ka = "12"

        # s'assurer que la valeur assignée est toujours un dictionnaire
        # with pytest.raises(TypeError):
        #     ObjDict("a")
        # ajout d'éléments avec la notation par point
        obj.x = {"y": 5}
        assert obj.x.y == 5

        # méthode select qui filtre les clés de l'objet.
        assert expected == obj.select(select_keys)

    def test_inspect_success_err(capsys):  # pylint: disable=unused-variable
        """
        Test inspect de l'objet.
        """
        obj = ObjDict({"a": 1, "b": 2})
        obj.inspect  # pylint: disable=pointless-statement
        captured = capsys.readouterr()
        assert captured.out == "{'a': 1, 'b': 2}\n"
        assert captured.err == ""

    def test_delattr(obj):  # pylint: disable=unused-variable
        """
        Test la suppression d'éléments avec del.
        """
        obj1 = ObjDict()
        obj1.test = "test_value"
        obj1.another_test = "another_test_value"

        # Suppression d'un attribut avec del
        del obj1.test

        # Vérifiez qu'une AttributeError est levée
        # lors de la tentative d'accès à l'attribut supprimé
        with pytest.raises(AttributeError):
            _ = obj1.test  # Essayer d'accéder à l'attribut supprimé
        # suppression d'éléments avec del
        del obj.test
        # lève une erreur KeyError lorsqu'un élément n'existe pas
        with pytest.raises(AttributeError):
            obj.test  # pylint: disable=pointless-statement

        with pytest.raises(AttributeError):
            del obj.non_existent_attribute

    def test_to_dict(sample_obj_dict):  # pylint: disable=unused-variable
        """
        Test la conversion en dictionnaire.
        """
        expected = {
            "name": "John",
            "age": 30,
            "address": {"street": "123 Main St", "city": "Anytown", "state": "CA"},
            "scores": [90, 80, 95],
        }
        assert sample_obj_dict.to_dict() == expected

    def test_from_dict():  # pylint: disable=unused-variable
        """
        Test la création d'un objet depuis un dictionnaire.
        """
        data = {
            "name": "John",
            "age": 30,
            "address": {"street": "123 Main St", "city": "Anytown", "state": "CA"},
            "scores": [90, 80, 95],
        }
        obj_dict = ObjDict.from_dict(data)
        assert obj_dict.to_dict() == data

    def test_update(sample_obj_dict):  # pylint: disable=unused-variable
        """
        Test la mise à jour de l'objet avec un dictionnaire.
        """
        data = {
            "name": "Jane",
            "age": 35,
            "address": {"street": "456 Second St", "city": "Othertown", "state": "MA"},
            "scores": [85, 95],
        }
        sample_obj_dict.update(data)
        expected = {
            "name": "Jane",
            "age": 35,
            "address": {
                "street": "456 Second St",
                "city": "Othertown",
                "state": "MA",
            },
            "scores": [85, 95],
        }
        assert sample_obj_dict.to_dict() == expected

    def test_items(sample_obj_dict):  # pylint: disable=unused-variable
        """
        Test l'accès aux éléments de l'objet sous forme de liste de tuples.
        """
        expected = [
            ("name", "John"),
            ("age", 30),
            ("address", {"street": "123 Main St", "city": "Anytown", "state": "CA"}),
            ("scores", [90, 80, 95]),
        ]
        assert sample_obj_dict.items() == expected

    def test_copy(sample_obj_dict):  # pylint: disable=unused-variable
        """
        Test la copie de l'objet.
        """
        copied_dict = sample_obj_dict.copy()
        assert copied_dict.to_dict() == sample_obj_dict.to_dict()
        assert copied_dict is not sample_obj_dict
        assert copied_dict["address"] is not sample_obj_dict["address"]
