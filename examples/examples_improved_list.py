# Import of the class ImprovedList and datetime
from imobject import ImprovedList
from datetime import datetime
from helpers import compare_document


# Creating an instance of the ImprovedList class with a simple list as argument
simple_list = ImprovedList([1, 2, 3])

# Returns the first item in the list or None if the list is empty
assert simple_list.first() == 1
assert ImprovedList([]).first() == None

# Specify the number of elements to return
assert simple_list.first(2) == [1, 2]

# Returns the last item in the list or None if the list is empty
assert ImprovedList([1, 2, 3]).last() == 3
assert ImprovedList([]).last() == None

# Specify the number of elements to return
assert ImprovedList([1, 2, 3]).last(2) == [2, 3]

# Call a method of the object
assert ImprovedList([1, 2, 3]).map(":__str__") == ["1", "2", "3"]

# Aapply a function to each item in the list
assert ImprovedList([1, 2, 3]).map(str) == ["1", "2", "3"]

# Call a method of the object that returns a bytes object
assert ImprovedList([1, 2, 3]).map(":to_bytes") == [b"\x01", b"\x02", b"\x03"]

# Apply the function to each item in the list and return a list of floating
assert ImprovedList([1, 2, 3]).map(float) == [1.0, 2.0, 3.0]

# Apply a custom operation to each item in the list
assert ImprovedList([1, 2, 3]).map(lambda x: x * 2) == [2, 4, 6]
assert ImprovedList([1, 2, 3]).map(lambda x: x**2) == [1, 4, 9]

# Call a method with an empty list
assert ImprovedList([]).map(float) == []


# Définition d'une classe Person avec des méthodes pour manipuler des attributs d'une instance de la classe
class Person:
    def __init__(self, name: str, age: int, salary: float, date: str):
        self.name = name
        self.age = age
        self.salary = salary
        self.date = datetime.strptime(date, "%Y-%m-%d")

    def __dict__(self):
        return {
            "name": self.name,
            "age": self.age,
            "salary": self.salary,
            "date": self.date,
        }

    @property
    def ret_name(self) -> str:
        return self.name

    def get_name(self) -> str:
        return self.name

    def upper_name(self) -> str:
        return self.name.upper()

    def get_age(self) -> int:
        return self.age

    def change_name(self, new_name: str) -> None:
        self.name = new_name

    def change_age(self, new_age: int) -> None:
        self.age = new_age

    def is_adult(self) -> bool:
        return self.age >= 18

    def set_name(self, new_name: str) -> None:
        self.name = new_name

    def __repr__(self) -> str:
        date = self.date.strftime("%Y-%m-%d")
        return f"Person(name='{self.name}', age={self.age}, salary={self.salary}, date='{date}')"


def sort_by_date(obj: Person) -> datetime:
    return obj.date


# Création d'une liste d'instances de la classe Person
people = [
    Person("Alice", 25, 100, "2022-01-05"),
    Person("Bob", 12, 364, "2021-12-25"),
    Person("Charlie", 35, 740, "2022-01-20"),
]

# Création d'une instance de la classe ImprovedList avec comme argument la liste de Person créée précédemment
person_list = ImprovedList(people)

# Call an object method directly on the elements of a list.
assert person_list.map(":upper_name") == ["ALICE", "BOB", "CHARLIE"]
assert person_list.map(":is_adult") == [True, False, True]
assert person_list.map(":get_age") == [25, 12, 35]

# Retrieve the object attributes from each instance within the list.
assert person_list.map(".name") == ["Alice", "Bob", "Charlie"]
assert person_list.map(".age") == [25, 12, 35]

# Apply custom operations to filtered elements of a list.
assert person_list.map(
    lambda x: x.get_name(), filter_func=lambda x: isinstance(x, Person) and x.age >= 30
) == ["Charlie"]
assert person_list.map(":get_name", filter_func=lambda x: isinstance(x, Person)) == [
    "Alice",
    "Bob",
    "Charlie",
]

# Map should get a object method (string start with ':') or object attribut (string start with '.')
try:
    person_list.map("name", filter_func=lambda x: isinstance(x, Person))
except TypeError as exc:
    assert (
        str(exc)
        == "called must be a string start with ':' for obj method or '.' obj attribute, or a callable"
    )

# Apply custom method to extract names sorted by date (costum function)
assert person_list.map(called=lambda obj: obj.name, sort_func=sort_by_date) == [
    "Bob",
    "Alice",
    "Charlie",
]

# Apply custom method to extract names sorted by date (costum function) and get objects
sorted_persons = person_list.map(called=lambda obj: obj, sort_func=sort_by_date)
expected_list = [
    Person(name="Bob", age=12, salary=364, date="2021-12-25"),
    Person(name="Alice", age=25, salary=100, date="2022-01-05"),
    Person(name="Charlie", age=35, salary=740, date="2022-01-20"),
]
assert compare_document(sorted_persons, expected_list)

# Apply custom operations to filtered elements of a mixed list.
data_list = person_list + ImprovedList(
    [1, 2, 3, 10, "four", 5.0, {"six": 6}, [7], "Apple", "Banana", "Orange"]
)
expected_list = [
    Person(name="Alice", age=25, salary=100, date="2022-01-05"),
    Person(name="Bob", age=12, salary=364, date="2021-12-25"),
    Person(name="Charlie", age=35, salary=740, date="2022-01-20"),
    1,
    2,
    3,
    10,
    "four",
    5.0,
    {"six": 6},
    [7],
    "Apple",
    "Banana",
    "Orange",
]
assert compare_document(expected_list, data_list)
assert data_list.map(
    called=lambda x: x**2, filter_func=lambda x: isinstance(x, int) and x % 2 == 0
) == [4, 100]
assert data_list.map(
    called=lambda x: x.upper(), filter_func=lambda x: isinstance(x, str) and len(x) > 5
) == ["BANANA", "ORANGE"]
assert data_list.map(
    called=lambda x: x.capitalize(),
    filter_func=lambda x: isinstance(x, str) and "a" in x.lower(),
) == ["Apple", "Banana", "Orange"]
assert data_list.map(
    called=str, filter_func=lambda x: isinstance(x, int) and x >= 3
) == ["3", "10"]

# Call an object method to change the name of Person objects
person_list.map(":change_name", **{"new_name": "Thor"})
expected_dict = [
    Person(name="Thor", age=25, salary=100, date="2022-01-05"),
    Person(name="Thor", age=12, salary=364, date="2021-12-25"),
    Person(name="Thor", age=35, salary=740, date="2022-01-20"),
]
assert compare_document(person_list, expected_dict)
