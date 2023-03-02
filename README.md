# imobject

If you want to make data handling easier in Python, you can use imobject. It is a library that has three helpful classes: `ObjDict`, `ImprovedList` and `OrmCollection`.

The `ObjDict` class allows you to create dictionary objects (Dictionary-like object or Dynamic Class as dict), which makes it easier to access and manipulate data elements. This class inherits from the built-in `dict` class and adds features such as converting dictionaries to objects, handling missing keys and access dictionary keys as attributes.

The `ImprovedList` class offers an improved alternative to the Python list class, which it provide additional methods for working with lists of `ObjDict`. This class extends the built-in `list` class and adds features such as inspecting the elements of a list and performing advanced mapping operations.

The `OrmCollection` class providing an interface and additional methods for querying and manipulating objects in the `ImprovedList`. This class is a list-like collection that extends `ImprovedList` and that implements an ORM overlay (wrapper) for a list of `ObjDict`.

# Exemples
## ObjDict
```python
>>> from imobject import ObjDict
>>> class Person:
        def __init__(self, name: str, age: int) -> None:
            self.name = name
            self.age = age
        def __repr__(self) -> str:
            return f"Person(name='{self.name}', age={self.age})"

>>> person = Person("zakaria", 33)
>>> obj = ObjDict({"a": 1, "test": {"zak": person}, "b": {"c": 2, "d": [3, 4]}})
>>> obj.a
1
>>> obj.select(['a'])
{'a': 1}
>>> res = obj.select(['a', 'b'])
>>> res
{'a': 1, 'b': {'c': 2, 'd': [3, 4]}}
>>> type(res)
<class 'imobject.obj_dict.ObjDict'>
>>> obj.select(1)
TypeError: Argument 'wanted_keys' should be a list, got 'int' instead.
>>> obj.select("d")
TypeError: Argument 'wanted_keys' should be a list, got 'str' instead.
>>> obj.select(["c"])
KeyError: "'ObjDict' object has no attribute 'c'"
>>> res.b
{'c': 2, 'd': [3, 4]}
>>> obj.select(['a', 'test'])
{'a': 1, 'test': {'zak': Person(name='zakaria', age=33)}}
>>> obj.select(['c'])
KeyError: "'ObjDict' object has no attribute 'c'"
>>> obj.a = 13
>>> obj.a
13
>>> obj['b']['c']
2
>>> obj.b.c
2
>>> obj.x = {"y": 5}
>>> obj.x
{"y": 5}
>>> obj.inspect
{   'a': 13,
    'b': {'c': 2, 'd': [3, 4]},
    'test': {'zak': Person(name='zakaria', age=33)},
    'x': {'y': 5}}
>>> del obj.a
>>> obj.a
AttributeError: 'ObjDict' object has no attribute 'a'
>>> obj_dict = obj.to_dict()
>>> obj_dict
{'test': {'zak': Person(name='zakaria', age=33)}, 'b': {'c': 2, 'd': [3, 4]}, 'x': {'y': 5}}
>>> type(obj_dict)
<class 'dict'>
>>> obj = ObjDict({
              "name": "Jane",
              "age": 35,
              "address": {"street": "456 Second St", "city": "Othertown", "state": "MA"},
              "scores": [85, 95],
          })
>>> obj
{'name': 'Jane', 'age': 35, 'address': {'street': '456 Second St', 'city': 'Othertown', 'state': 'MA'}, 'scores': [85, 95]}
>>> obj.update({
              "name": "Will",
              "age": 50,
              "address": {"street": "456 Second St", "city": "Othertown", "state": "LA"},
              "scores": [85, 100],
          })
>>> obj
{'name': 'Will', 'age': 50, 'address': {'street': '456 Second St', 'city': 'Othertown', 'state': 'LA'}, 'scores': [85, 100]}
>>> obj.items()
[('name', 'Will'), ('age', 50), ('address', {'street': '456 Second St', 'city': 'Othertown', 'state': 'LA'}), ('scores', [85, 100])]
>>> copied_dict = obj.copy()
>>> copied_dict
{'name': 'Will', 'age': 50, 'address': {'street': '456 Second St', 'city': 'Othertown', 'state': 'LA'}, 'scores': [85, 100]}
```
## ImprovedList
```python
>>> from imobject import ImprovedList
>>> simple_list = ImprovedList([1, 2, 3])
>>> simple_list.first()
1
>>> simple_list.first(2)
[1, 2]
>>> ImprovedList([]).first() # None
>>> ImprovedList([1, 2, 3]).last()
3
>>> ImprovedList([1, 2, 3]).last(2)
[2, 3]
>>> ImprovedList([]).last() # None
>>> ImprovedList([1, 2, 3]).map(":__str__")
['1', '2', '3']
>>> ImprovedList([1, 2, 3]).map(str)
['1', '2', '3']
>>> ImprovedList([1, 2, 3]).map(":to_bytes")
[b'\x01', b'\x02', b'\x03']
>>> ImprovedList([1, 2, 3]).map(float)
[1.0, 2.0, 3.0]
>>> ImprovedList([1, 2, 3]).map(lambda x: x * 2)
[2, 4, 6]
>>> ImprovedList([1, 2, 3]).map(lambda x: x ** 2)
[1, 4, 9]
>>> ImprovedList([]).map(float)
[]
>>> class Person:
        def __init__(self, name: str, age: int, salary: float):
            self.name = name
            self.age = age
            self.salary = salary
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
            return f"Person(name='{self.name}', age={self.age}, salary={self.salary})"
>>> people = [
             Person("Alice", 25, 100),
             Person("Bob", 12, 364),
             Person("Charlie", 35, 740),
         ]
>>> person_list = ImprovedList(people)
>>> person_list.map(':upper_name')
['ALICE', 'BOB', 'CHARLIE']
>>> person_list.map(":is_adult")
[True, False, True]
>>> person_list.map(":get_age")
[25, 12, 35]
>>> person_list.map(".name")
['Alice', 'Bob', 'Charlie']
>>> person_list.map(".age")
[25, 12, 35]
>>> person_list.map(":change_name", **{"new_name": "Thor"})
[None, None, None]
>>> person_list.map(lambda x: x.get_name(), filter_func=lambda x: isinstance(x, Person) and x.age >= 30)
['Charlie']
>>> person_list.map(":get_name", filter_func=lambda x: isinstance(x, Person))
['Alice', 'Bob', 'Charlie']
>>> person_list.map(".name", filter_func=lambda x: isinstance(x, Person))
['Alice', 'Bob', 'Charlie']
>>> person_list.inspect
ImprovedList(Person) data:
Person(name='Thor', age=25, salary=100)
Person(name='Thor', age=12, salary=364)
Person(name='Thor', age=35, salary=740)
>>> person_list.map(":change_name", **{"new_name": ""})
[None, None, None]
>>> person_list.inspect
ImprovedList(Person) data:
Person(name='', age=25, salary=100)
Person(name='', age=12, salary=364)
Person(name='', age=35, salary=740)
```
## OrmCollection