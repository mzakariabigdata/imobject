"""
Module de test pour la classe ObjectFactory.
"""
import pytest
from imobject import ObjectFactory


# Exemple de classes pour les tests
class Parent:  # pylint: disable=too-few-public-methods
    """Classe Parent pour les tests."""

    def __init__(self, name):
        self.name = name


class Child:  # pylint: disable=too-few-public-methods
    """Classe Child pour les tests."""

    def __init__(self, age):
        self.age = age


# Exemple de configuration pour les tests
test_conf = {
    "class": "parent",
    "params": {"name": "Parent1"},
    "child": {"class": "child", "params": {"age": 5}},
    "children": [
        {"class": "child", "params": {"age": 6}},
        {"class": "child", "params": {"age": 7}},
    ],
}

class_map = {
    "parent": Parent,
    "child": Child,
}


# Test pour vérifier la création d'objets
@pytest.mark.parametrize(
    "conf, class_map, expected_class", [(test_conf, class_map, Parent)]
)
def test_object_creation(
    conf, class_map, expected_class
):  # pylint: disable=redefined-outer-name
    """Teste la méthode create_object de la classe ObjectFactory."""

    factory = ObjectFactory(conf, class_map)
    obj = factory.get_object()
    assert isinstance(obj, expected_class)


# Test pour vérifier la gestion d'erreurs lors de la création d'objets
def test_object_creation_error():
    """Teste error create_object de la classe ObjectFactory."""

    conf = {"class": "unknown_class"}
    factory = ObjectFactory(conf, class_map)
    with pytest.raises(ValueError):
        factory.get_object()


# Test pour vérifier les propriétés dynamiques
def test_dynamic_properties():
    """Teste les propriétés dynamiques créées par la classe ObjectFactory."""

    factory = ObjectFactory(test_conf, class_map)
    parent_obj = factory.get_object()

    # Vérification des propriétés pour 'child'
    assert parent_obj.child.age == Child(age=5).age
    parent_obj.child = Child(10)
    assert parent_obj.child.age == Child(age=10).age

    # Vérification des propriétés pour 'children'
    assert [child.age for child in parent_obj.children] == [
        Child(age=6).age,
        Child(age=7).age,
    ]
    parent_obj.children = [Child(8), Child(9)]
    assert [child.age for child in parent_obj.children] == [
        Child(age=8).age,
        Child(age=9).age,
    ]
