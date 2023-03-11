# Importer la classe ObjDict
from imobject import ObjDict
from helpers import compare_document


# Define a Person class with two attributes: name and age
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        return f"Person(name='{self.name}', age={self.age})"

    def __dict__(self):
        return {"name": self.name, "age": self.age}


# Create an instance of the Person class
person = Person("zakaria", 33)

# Create an ObjDict class instance with a nested dictionary
obj = ObjDict({"a": 1, "test": {"zak": person}, "b": {"c": 2, "d": [3, 4]}})

# Access a specific attribute of the object obj
assert obj.a == 1

# Select a subset of attributes of the object obj
assert obj.select(["a"]) == {"a": 1}
assert obj.select(["a", "b"]) == {"a": 1, "b": {"c": 2, "d": [3, 4]}}
assert type(obj.select(["a", "b"])) == ObjDict

# Try to access a non-existent attribute or pass an invalid argument type
try:
    obj.select(1)
except TypeError as exc:
    assert str(exc) == "Argument 'wanted_keys' should be a list, got 'int' instead."

try:
    obj.select("d")
except TypeError as exc:
    assert str(exc) == "Argument 'wanted_keys' should be a list, got 'str' instead."

try:
    obj.select(["c"])
except KeyError as exc:
    assert exc.args[0] == "'ObjDict' object has no attribute 'c'"

# Access a nested attribute
assert obj.b == {"c": 2, "d": [3, 4]}

# Select a subset of attributes with class instances
expected = {"a": 1, "test": {"zak": Person(name="zakaria", age=33)}}
result = obj.select(["a", "test"])
assert compare_document(result, expected)

# Edit an existing attribute
obj.a = 13
assert obj.a == 13

# Access an attribute through an index key
assert obj["b"]["c"] == 2

# Access a nested attribute through points
assert obj.b.c == 2

# Add a new attribute
obj.x = {"y": 5}
assert obj.x == {"y": 5}

# Show all attributes of the object obj
expected_dict = {
    "a": 13,
    "b": {"c": 2, "d": [3, 4]},
    "test": {"zak": Person(name="zakaria", age=33)},
    "x": {"y": 5},
}
assert compare_document(obj.inspect, expected_dict)

# Delete an existing attribute
del obj.a
try:
    obj.a
except AttributeError as e:
    assert str(e) == "'ObjDict' object has no attribute 'a'"

# Convert object to dictionary
obj_dict = obj.to_dict()
expected_dict = {
    "test": {"zak": Person(name="zakaria", age=33)},
    "b": {"c": 2, "d": [3, 4]},
    "x": {"y": 5},
}
assert compare_document(obj_dict, expected_dict)

# Update some values in the object dictionary
obj = ObjDict(
    {
        "name": "Jane",
        "age": 35,
        "address": {"street": "456 Second St", "city": "Othertown", "state": "MA"},
        "scores": [85, 95],
    }
)
obj.update(
    {
        "name": "Will",
        "age": 50,
        "address": {"street": "456 Second St", "city": "Othertown", "state": "LA"},
        "scores": [85, 100],
    }
)

# Verify the object dictionary is updated correctly
assert obj == {
    "name": "Will",
    "age": 50,
    "address": {"street": "456 Second St", "city": "Othertown", "state": "LA"},
    "scores": [85, 100],
}

# Get a list of items in the object dictionary
assert list(obj.items()) == [
    ("name", "Will"),
    ("age", 50),
    ("address", {"street": "456 Second St", "city": "Othertown", "state": "LA"}),
    ("scores", [85, 100]),
]

# Make a copy of the object dictionary
copied_dict = obj.copy()

# Verify the copied dictionary is created correctly
assert copied_dict == {
    "name": "Will",
    "age": 50,
    "address": {"street": "456 Second St", "city": "Othertown", "state": "LA"},
    "scores": [85, 100],
}
