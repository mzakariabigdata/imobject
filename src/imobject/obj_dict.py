"""
This module contains the `ObjDict` class, which provides a dictionary-like interface to access 
object attributes.

`ObjDict` is similar to a dictionary in that it allows you to access values using keys, but it
 also allows you to access values using dot notation for attribute-like access. It is particularly
   useful when working with JSON data or when you want to treat an object like a dictionary.

Example usage:

    >>> obj = ObjDict({'a': 1, 'b': {'c': 2}})
    >>> obj.a
    1
    >>> obj['b']['c']
    2
    >>> obj.b.c
    2

The `ObjDict` class inherits from the `dict` class, so all the usual dictionary methods 
    (e.g., `keys()`, `values()`, `items()`) are available.

Note that when you use dot notation to access an attribute, if the attribute doesn't exist,
 `ObjDict` will create it for you.

"""
import pprint


# class ObjDictException(AttributeError):
#     """Associated objdixt Exception"""


class ObjDict(dict):
    """
    Dynamic Class as dict
    A dictionary-like object that allows access to keys as attributes.
    This class inherits from the built-in `dict` class and adds the ability
     to access dictionary keys as attributes.

    Example usage:
        >>> my_dict = {'name': 'Alice', 'age': 25}
        >>> obj_dict = ObjDict(my_dict)
        >>> print(obj_dict.name)
        Alice
        >>> obj_dict.age = 30
        >>> print(obj_dict['age'])
        30

    Attributes:
        __dict__: A dictionary holding the object's attributes.
    """

    def __getattr__(self, name: str):
        """Get attribute value"""
        if name not in self:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
        return self._clean_item(self[name])

    def __setattr__(self, name: str, value):
        """Set Any attribute value"""
        # Convertir les dictionnaires en ObjDict
        from imobject.improved_list import (  # pylint: disable=import-outside-toplevel
            ImprovedList,
        )

        if isinstance(value, dict) and not isinstance(value, ObjDict):
            value = ObjDict(value)
        # Convertir les listes en ImprovedList
        elif isinstance(value, list) and not isinstance(value, ImprovedList):
            value = ImprovedList(value)
        super().__setattr__(name, value)
        self[name] = value

    def __delattr__(self, name: str):
        """Delete attribute"""
        try:
            del self[name]
        except KeyError as exc:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            ) from exc

    def to_dict(self) -> dict:
        """Return a dictionary representation of the object"""
        from imobject.orm_collection import (  # pylint: disable=import-outside-toplevel
            OrmCollection,
        )

        result = {}
        for key, value in self.items():
            if isinstance(value, ObjDict):
                result[key] = value.to_dict()
            elif isinstance(value, OrmCollection):  # Ajouté cette partie
                result[key] = list(value)  # Convertir OrmCollection en liste
            else:
                result[key] = value
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "ObjDict":
        """Create an object from a dictionary"""
        result = cls()
        for key, value in data.items():
            result[key] = cls._clean_item(value)
        return result

    def update(self, data: dict):
        """Update the object with a dictionary"""
        for key, value in data.items():
            self[key] = self._clean_item(value)

    def items(self):
        """Return the keys and values of the object as tuples"""
        return [(key, self._clean_item(value)) for key, value in super().items()]

    def copy(self) -> "ObjDict":
        """Return a deep copy of the object"""
        return self.__class__(self.to_dict())

    @property
    def inspect(self):
        """Return a pretty formatted information of object"""
        pprint.pprint(self, indent=4)
        return self

    def select(self, wanted_keys: list) -> "ObjDict":
        """Filter dict by returning only some keys"""
        if not isinstance(wanted_keys, list):
            raise TypeError(
                f"Argument 'wanted_keys' should be a list, "
                f"got '{type(wanted_keys).__name__}' instead."
            )
        selected_items = {}
        for key in wanted_keys:
            if not isinstance(key, str):
                raise TypeError(f"Element {key} in 'wanted_keys' list is not a string")
            try:
                selected_items[key] = self[key]
            except KeyError as exc:
                raise KeyError(
                    f"'{self.__class__.__name__}' object has no attribute '{key}'"
                ) from exc
        return self.__class__(selected_items)

    @staticmethod
    def _clean_item(item):
        """Improve type of object"""
        if isinstance(item, dict) and not isinstance(item, ObjDict):
            return ObjDict(item)
        if isinstance(item, list):
            from imobject.orm_collection import (  # pylint: disable=import-outside-toplevel
                OrmCollection,
            )

            return OrmCollection(item)
        return item
