# Importer la classe OrmCollection
import re
from imobject import (
    OrmCollection,
    ObjDict,
    Query,
    Filter,
    BaseMultipleFound,
    BaseNotFound,
)

# Create an instance of the OrmCollection class with data
orm_collection = OrmCollection(
    [
        ObjDict(
            {
                "name": "Alice",
                "age": 25,
                "gender": "female",
                "occupation": "psychologist",
            }
        ),
        ObjDict(
            {"name": "Bob", "age": 40, "gender": "male", "occupation": "CIA agent"}
        ),
        {"name": "Charlie", "age": 30, "gender": "male", "occupation": "student"},
        {"name": "Dave", "age": 30, "gender": "male", "occupation": "engineer"},
    ]
)

my_orm_collection_group = OrmCollection(
    [
        {"name": "Alice", "age": 25, "gender": "female", "occupation": "psy"},
        {"name": "Alice", "age": 80, "gender": "male", "occupation": "retraite"},
        {"name": "Bob", "age": 40, "gender": "male", "occupation": "cia"},
        {"name": "Charlie", "age": 30, "gender": "male", "occupation": "etud"},
        {"name": "Charlie", "age": 30, "gender": "male", "occupation": "prof"},
        {"name": "Dave", "age": 30, "gender": "male", "occupation": "ing"},
        {"name": "Dave", "age": 31, "gender": "male", "occupation": "prof"},
    ]
)

# Find all elements with name 'Alice'
results = orm_collection.where(name="Alice")
assert len(results) == 1
assert results[0] == {
    "name": "Alice",
    "age": 25,
    "gender": "female",
    "occupation": "psychologist",
}

# Find all elements where age is greater than 30 and occupation contains the word 'agent'
results = orm_collection.where(age__gt=30, occupation__contains="agent")
assert len(results) == 1
assert results[0] == {
    "name": "Bob",
    "age": 40,
    "gender": "male",
    "occupation": "CIA agent",
}

# Find all elements where age is not equal to 30
results = orm_collection.where(age__not=30)
assert len(results) == 2
assert results[0] == {
    "name": "Alice",
    "age": 25,
    "gender": "female",
    "occupation": "psychologist",
}
assert results[1] == {
    "name": "Bob",
    "age": 40,
    "gender": "male",
    "occupation": "CIA agent",
}

# Find all elements where name contains the letter 'a' and occupation starts with the letter 'p'
results = orm_collection.where(name__contains="c", occupation__startswith="p")
assert len(results) == 1
assert results[0] == {
    "name": "Alice",
    "age": 25,
    "gender": "female",
    "occupation": "psychologist",
}

# Trouver tous les éléments avec le nom commençant par "A" ou se terminant par "e"
results = orm_collection.where(name=re.compile(r"^A.*|.*e$"))
assert len(results) == 3
assert all(result["name"] in {"Alice", "Charlie", "Dave"} for result in results)

# Trouver tous les éléments avec le nom commençant par "A"
results = orm_collection.where(name=re.compile(r"^A.*"))
assert len(results) == 1
assert results[0]["name"] == "Alice"

# Trouver tous les éléments avec le nom se terminant par "e"
results = orm_collection.where(name=".*e$")
assert len(results) == 3
assert all(result["name"] in {"Alice", "Charlie", "Dave"} for result in results)

# Trouver tous les éléments avec un nom vide (devrait renvoyer tous les éléments)
results = orm_collection.where(name="")
print(results, len(results), len(orm_collection))
assert len(results) == len(orm_collection)
assert all(result in orm_collection for result in results)

# Trouver tous les éléments sans paramètres (devrait renvoyer 0 éléments)
results = orm_collection.where()
assert len(results) == 0

# Trouver tous les éléments avec l'âge égal à 100 (devrait renvoyer un ensemble vide)
results = orm_collection.where(age=100)
assert len(results) == 0

# Trouver tous les éléments avec le nom contenant la lettre "z"
results = orm_collection.where(name=re.compile(r".z.", re.IGNORECASE))
assert len(results) == 0

# Trouver tous les éléments avec le nom contenant la lettre "a" ou "e"
results = orm_collection.where(name=r"*a*|*e*")
# assert len(results) == 3
# assert all(result["name"] in {"Alice", "Charlie", "Dave"} for result in results)

# Trouver tous les éléments avec le nom se terminant par "ie"
results = orm_collection.where(name=re.compile(r".*ie$", re.IGNORECASE))
assert len(results) == 1
assert results[0]["name"] == "Charlie"

# Find all elements where age is greater than or equal to 30 and name contains 'v'
results = orm_collection.where(age__gte=30, name__contains="v")
assert len(results) == 1
assert results[0]["name"] == "Dave"

# Find all elements where age is not 25 and name contains 'v'
results = orm_collection.where(age__nin=[25], name__contains="v")
assert len(results) == 1
assert results[0]["name"] == "Dave"

# Find all elements where age is not 25 and name ends with 'e'
results = orm_collection.where(age__nin=[25], name__endswith="e")
assert len(results) == 2
assert {result["name"] for result in results} == {"Dave", "Charlie"}

# Find all elements with age equal to 25
results = orm_collection.where(age=25)
assert len(results) == 1
assert results[0]["name"] == "Alice"

# Find all elements with gender 'male' and age equal to 30
results = orm_collection.where(gender="male", age=30)
assert len(results) == 2
assert {result["name"] for result in results} == {"Charlie", "Dave"}

# Find all elements with name containing letter 'a'
results = orm_collection.where(name__contains="a")
assert len(results) == 2
assert {result["name"] for result in results} == {"Charlie", "Dave"}

# Find all elements where age is greater than 25 and name contains 'v'
results = orm_collection.where(age__gt=25, name__contains="v")
assert len(results) == 1
assert results[0]["name"] == "Dave"

# Find all elements where age is either 25 or 30 and name contains 'v'
results = orm_collection.where(age__in=[25, 30], name__contains="v")
assert len(results) == 1
assert results[0]["name"] == "Dave"

# Find all elements where age is less than 40 and name contains 'v'
results = orm_collection.where(age__lt=40, name__contains="v")
assert len(results) == 1
assert results[0]["name"] == "Dave"

# Find all elements where age is not 40 and name contains 'v'
results = orm_collection.where(age__not=40, name__contains="v")
assert len(results) == 1
assert results[0]["name"] == "Dave"

# Find all elements where age is equal to 40 and name contains 'b'
results = orm_collection.where(age__eq=40, name__contains="b")
assert len(results) == 1
assert results[0]["name"] == "Bob"

# Find all elements where age is less than or equal to 30 and name contains 'v'
results = orm_collection.where(age__lte=30, name__contains="v")
assert len(results) == 1
assert results[0]["name"] == "Dave"

# Test TypeError pour l'opérateur 'gt' avec une chaîne de caractères
try:
    orm_collection.where(**{"age__gt": "25"})
except TypeError as error:
    assert (
        error.args[0]
        == "Invalid type for value of '>' operator : expected int, found str"
    )

# Test TypeError pour l'opérateur 'in' avec un int
try:
    orm_collection.where(**{"age__in": 25})
except TypeError as error:
    assert (
        error.args[0]
        == "Invalid type for value of 'in' operator : expected list, found int"
    )

# Test TypeError pour l'opérateur 'contains' avec un int
try:
    orm_collection.where(**{"age__contains": 25})
except TypeError as error:
    assert str(error) == "'contains' lookup only works for string type fields"

# Test TypeError pour l'opérateur 'startswith' avec un int
try:
    orm_collection.where(**{"age__startswith": 25})
except TypeError as error:
    assert str(error) == "'startswith' lookup only works for string type fields"

# Test TypeError pour l'opérateur 'eq' avec une chaîne de caractères
try:
    orm_collection.where(**{"age__eq": "25"})
except TypeError as error:
    assert (
        str(error) == "'==' operator only works for same type fields, found int and str"
    )

# Test ValueError pour un opérateur invalide
try:
    orm_collection.where(Query([Filter("age", "test_not_op", 30)]))
except ValueError as error:
    assert str(error) == "'test_not_op' is not a valid operator"

# Recherche des éléments avec l'âge égal à 30
query = Query([Filter("age", None, 30)])
expected_names = {"Charlie", "Dave"}
results = orm_collection.where(query)

# Define query to find all elements with gender equal to male AND age equal to 30 with Query
query = Query([Filter("age", None, 30), Filter("gender", None, "male")])
results = orm_collection.where(query)
assert results == [
    {"name": "Charlie", "age": 30, "gender": "male", "occupation": "student"},
    {"name": "Dave", "age": 30, "gender": "male", "occupation": "engineer"},
]

# Define query to find all elements with gender equal to male AND age equal to 30 with Query
query = Query([Filter("age", None, 30)]) & Query([Filter("age", None, 30)])
results = orm_collection.where(query)
assert results == [
    {"name": "Charlie", "age": 30, "gender": "male", "occupation": "student"},
    {"name": "Dave", "age": 30, "gender": "male", "occupation": "engineer"},
]

# Define query to find all elements with gender equal to male OR age equal to 30 with Query
query = Query([Filter("age", None, 30)]) | Query([Filter("age", None, 40)])
results = orm_collection.where(query)
assert results == [
    {"name": "Bob", "age": 40, "gender": "male", "occupation": "CIA agent"},
    {"name": "Charlie", "age": 30, "gender": "male", "occupation": "student"},
    {"name": "Dave", "age": 30, "gender": "male", "occupation": "engineer"},
]

# Test ValueError pour un paramètre invalide
try:
    orm_collection.where(**{"name__notValid": "i"})
except ValueError as error:
    assert str(error) == "'notValid' is not a valid operator"

try:
    orm_collection.find_by(name=".*a.*")
    assert (
        False
    ), "Le test a échoué, car plusieurs éléments ont été trouvés avec le nom contenant 'a'."
except BaseMultipleFound:
    pass

try:
    orm_collection.find_by(age=20)
    assert (
        False
    ), "Le test a échoué, car aucun élément n'a été trouvé avec l'âge égal à 20."
except BaseNotFound:
    pass

# should return only one result
result = None
try:
    result = orm_collection.find_by(name__contains="v")
except BaseMultipleFound:
    assert (
        False
    ), "Le test a échoué, car plusieurs éléments ont été trouvés avec le nom contenant 'v'."
except BaseNotFound:
    assert (
        False
    ), "Le test a échoué, car aucun élément n'a été trouvé avec le nom contenant 'v'."
assert result == {"name": "Dave", "age": 30, "gender": "male", "occupation": "engineer"}

# Group element by attributs
results = my_orm_collection_group.group_by(lambda x: x.age)
assert len(results) == 5
assert set(results.keys()) == {25, 30, 80, 31, 40}

results = my_orm_collection_group.group_by(lambda x: x.occupation)
assert len(results) == 6
assert set(results.keys()) == {"psy", "retraite", "cia", "etud", "ing", "prof"}

# Group element by two attributs
results = orm_collection.group_by(lambda x: (x.gender, x.age))
assert len(results) == 3
assert results == {
    ("female", 25): [
        {"name": "Alice", "age": 25, "gender": "female", "occupation": "psychologist"}
    ],
    ("male", 40): [
        {"name": "Bob", "age": 40, "gender": "male", "occupation": "CIA agent"}
    ],
    ("male", 30): [
        {"name": "Charlie", "age": 30, "gender": "male", "occupation": "student"},
        {"name": "Dave", "age": 30, "gender": "male", "occupation": "engineer"},
    ],
}
assert set(results.keys()) == {
    ("female", 25),
    ("male", 40),
    ("male", 30),
}

# Créer une liste de noms
noms = ["Alice", "Bob", "Charlie", "David", "Edward"]

# Créer une collection ORM à partir de la liste
orm_collection_list = OrmCollection(noms)

# Grouper les noms par leur première lettre
results = orm_collection_list.group_by(lambda x: x[0])

# Vérifier les résultats attendus
assert results == {
    "A": ["Alice"],
    "B": ["Bob"],
    "C": ["Charlie"],
    "D": ["David"],
    "E": ["Edward"],
}

# Créer une liste de nombres
nombres = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Créer une collection ORM à partir de la liste
orm_collection_list = OrmCollection(nombres)

# Grouper les nombres pairs et impairs
results = orm_collection_list.group_by(lambda x: x % 2 == 0)
assert results == {True: [2, 4, 6, 8, 10], False: [1, 3, 5, 7, 9]}


# Trier une liste d'objets de la plus jeune à la plus âgée
people = [
    {"name": "Alice", "age": 25, "gender": "female"},
    {"name": "Bob", "age": 40, "gender": "male"},
    {"name": "Charlie", "age": 30, "gender": "male"},
    {"name": "Dave", "age": 30, "gender": "male"},
]
ordered_people = orm_collection.order_by("age")
assert ordered_people == [
    {"name": "Alice", "age": 25, "gender": "female", "occupation": "psychologist"},
    {"name": "Charlie", "age": 30, "gender": "male", "occupation": "student"},
    {"name": "Dave", "age": 30, "gender": "male", "occupation": "engineer"},
    {"name": "Bob", "age": 40, "gender": "male", "occupation": "CIA agent"},
]

# Trier une liste d'objets par ordre alphabétique de leur nom :
people = [
    {"name": "Alice", "age": 25, "gender": "female"},
    {"name": "Bob", "age": 40, "gender": "male"},
    {"name": "Charlie", "age": 30, "gender": "male"},
    {"name": "Dave", "age": 30, "gender": "male"},
]
ordered_people = orm_collection.order_by(lambda x: x["name"])
assert ordered_people == [
    {"name": "Alice", "age": 25, "gender": "female", "occupation": "psychologist"},
    {"name": "Bob", "age": 40, "gender": "male", "occupation": "CIA agent"},
    {"name": "Charlie", "age": 30, "gender": "male", "occupation": "student"},
    {"name": "Dave", "age": 30, "gender": "male", "occupation": "engineer"},
]

# Trier la liste par ordre alphabétique
lst = OrmCollection(["apple", "banana", "orange", "f", "pear", "c'est encore moi"])
ordered_lst = lst.order_by()
assert ordered_lst == ["f", "pear", "apple", "banana", "orange", "c'est encore moi"]

# Trier la liste
lst = OrmCollection([4, 2, 1, 3])
ordered_lst = lst.order_by()
assert ordered_lst == [1, 2, 3, 4]


# Lancer une erreur pour une clé de tri invalide
try:
    orm_collection.order_by(123)
except TypeError:
    pass

try:
    orm_collection.order_by(None)
except ValueError:
    pass

# Tri d'une liste d'objets par l'âge décroissant
ordered_lst = orm_collection.order_by(lambda x: -x["age"])
assert ordered_lst == [
    {"name": "Bob", "age": 40, "gender": "male", "occupation": "CIA agent"},
    {"name": "Charlie", "age": 30, "gender": "male", "occupation": "student"},
    {"name": "Dave", "age": 30, "gender": "male", "occupation": "engineer"},
    {"name": "Alice", "age": 25, "gender": "female", "occupation": "psychologist"},
]
# Tri d'une liste d'objets par l'âge décroissant
results = OrmCollection([4, 2, 1, 3]).order_by(lambda x: -x)
# Vérifier les résultats attendus
assert results == [4, 3, 2, 1]


# Utiliser la méthode all() pour récupérer tous les éléments
all_elements = orm_collection.all()
assert all_elements == [
    {"name": "Alice", "age": 25, "gender": "female", "occupation": "psychologist"},
    {"name": "Bob", "age": 40, "gender": "male", "occupation": "CIA agent"},
    {"name": "Charlie", "age": 30, "gender": "male", "occupation": "student"},
    {"name": "Dave", "age": 30, "gender": "male", "occupation": "engineer"},
]

# Utiliser la méthode offset() pour récupérer les éléments à partir de l'index 2
offset_elements = orm_collection.offset(2)
assert offset_elements == [
    {"name": "Charlie", "age": 30, "gender": "male", "occupation": "student"},
    {"name": "Dave", "age": 30, "gender": "male", "occupation": "engineer"},
]

# Utiliser la méthode limit() pour récupérer les deux premiers éléments
limit_elements = orm_collection.limit(2)
assert limit_elements == [
    {"name": "Alice", "age": 25, "gender": "female", "occupation": "psychologist"},
    {"name": "Bob", "age": 40, "gender": "male", "occupation": "CIA agent"},
]

lst = OrmCollection([1, 2, 3, 4])
distinct_lst = lst.distinct()
assert distinct_lst == [1, 2, 3, 4]

lst = OrmCollection([1, 2, 2, 3, 4, 4])
distinct_lst = lst.distinct()
assert distinct_lst == [1, 2, 3, 4]

lst = OrmCollection(["apple", "banana", "orange", "f", "pear", "orange"])
distinct_lst = lst.distinct()
assert distinct_lst == ["apple", "banana", "orange", "f", "pear"]

orm_collection = OrmCollection(
    [
        {"name": "Alice", "age": 25, "gender": "female", "taf": "psy"},
        {"name": "Alice", "age": 80, "gender": "male", "taf": "retraite"},
        {"name": "Bob", "age": 40, "gender": "male", "taf": "cia"},
        {"name": "Charlie", "age": 30, "gender": "male", "taf": "etud"},
        {"name": "Charlie", "age": 30, "gender": "male", "taf": "prof"},
        {"name": "Dave", "age": 30, "gender": "male", "taf": "ing"},
        {"name": "Dave", "age": 31, "gender": "male", "taf": "chomor"},
    ]
)
distinct_coll = orm_collection.distinct("name", "age")
assert len(distinct_coll) == 6
assert {(person["name"], person["age"]) for person in distinct_coll} == {
    ("Alice", 25),
    ("Alice", 80),
    ("Dave", 30),
    ("Dave", 31),
    ("Bob", 40),
    ("Charlie", 30),
}
