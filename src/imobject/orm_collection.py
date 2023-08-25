# pylint: disable=missing-function-docstring, unnecessary-lambda, line-too-long
"""
Module providing the `OrmCollection` class, which allows easy querying and filtering of collections of objects.

The `OrmCollection` class is designed to work with any iterable of objects, providing a simple and consistent interface for filtering, sorting, and transforming the collection.
It allows for the use of chained queries, so that multiple filters and transformations can be applied to a collection in a single statement.

"""
import re
from typing import Any, List, Union, Dict
from collections import OrderedDict
from imobject.improved_list import ImprovedList
from imobject.exception import BaseMultipleFound, BaseNotFound


class Filter:
    """
    A helper class for creating filters on collections of data.

    This class provides several static methods for performing common filtering operations,
    such as checking if a value is less than another value, or checking if a string starts
    with a certain prefix.

    Attributes:
        op_funcs (Dict[str, Callable[[Any, Any], bool]]): A dictionary of filter operation
            functions, mapping operation names to their corresponding functions.

    Methods:
        less_than(first_operand: Any, second_operand: Any) -> bool:
            Returns True if the first operand is less than the second operand, otherwise raises a TypeError.

        greater_than(first_operand: Any, second_operand: Any) -> bool:
            Returns True if the first operand is greater than the second operand, otherwise raises a TypeError.

        less_than_or_equal_to(first_operand: Any, second_operand: Any) -> bool:
            Returns True if the first operand is less than or equal to the second operand, otherwise raises a TypeError.

        greater_than_or_equal_to(first_operand: Any, second_operand: Any) -> bool:
            Returns True if the first operand is greater than or equal to the second operand, otherwise raises a TypeError.

        equal_to(first_operand: Any, second_operand: Any) -> bool:
            Returns True if the first operand is equal to the second operand, otherwise raises a TypeError.

        not_equal_to(first_operand: Any, second_operand: Any) -> bool:
            Returns True if the first operand is not equal to the second operand, otherwise raises a TypeError.

        in_list(first_operand: Any, second_operand: Union[List, Tuple]) -> bool:
            Returns True if the first operand is in the second operand list, otherwise raises a TypeError.

        not_in_list(first_operand: Any, second_operand: Union[List, Tuple]) -> bool:
            Returns True if the first operand is not in the second operand list, otherwise raises a TypeError.

        starts_with(first_operand: str, second_operand: str) -> bool:
            Returns True if the first string starts with the second string, otherwise raises a TypeError.

        ends_with(first_operand: str, second_operand: str) -> bool:
            Returns True if the first string ends with the second string, otherwise raises a TypeError.

        contains_string(first_operand: str, second_operand: str) -> bool:
            Returns True if the first string contains the second string, otherwise raises a TypeError.

        raise_type_error(operation: str, first_operand: Any, second_operand: Any) -> None:
            Raises a TypeError with a message indicating that the given operation is not valid
            for the types of the first and second operands.
    """

    op_funcs = {
        "lt": lambda first_operand, second_operand: Filter.less_than(
            first_operand, second_operand
        ),
        "gt": lambda first_operand, second_operand: Filter.greater_than(
            first_operand, second_operand
        ),
        "endswith": lambda first_operand, second_operand: Filter.ends_with(
            first_operand, second_operand
        ),
        "startswith": lambda first_operand, second_operand: Filter.starts_with(
            first_operand, second_operand
        ),
        "in": lambda first_operand, second_operand: Filter.in_list(
            first_operand, second_operand
        ),
        "contains": lambda first_operand, second_operand: Filter.contains_string(
            first_operand, second_operand
        ),
        "nin": lambda first_operand, second_operand: Filter.not_in_list(
            first_operand, second_operand
        ),
        "not": lambda first_operand, second_operand: Filter.not_equal_to(
            first_operand, second_operand
        ),
        "eq": lambda first_operand, second_operand: Filter.equal_to(
            first_operand, second_operand
        ),
        "lte": lambda first_operand, second_operand: Filter.less_than_or_equal_to(
            first_operand, second_operand
        ),
        "gte": lambda first_operand, second_operand: Filter.greater_than_or_equal_to(
            first_operand, second_operand
        ),
    }

    @staticmethod
    def less_than(first_operand: Any, second_operand: Any) -> bool:
        if isinstance(first_operand, type(second_operand)):
            return first_operand < second_operand
        return Filter.raise_type_error("<", first_operand, second_operand)

    @staticmethod
    def greater_than(first_operand: Any, second_operand: Any) -> bool:
        if isinstance(first_operand, type(second_operand)):
            return first_operand > second_operand
        return Filter.raise_type_error(">", first_operand, second_operand)

    @staticmethod
    def ends_with(first_operand: str, second_operand: str) -> bool:
        if isinstance(first_operand, str) and isinstance(second_operand, str):
            return first_operand.endswith(second_operand)
        return Filter.raise_type_error("endswith", first_operand, second_operand)

    @staticmethod
    def starts_with(first_operand: str, second_operand: str) -> bool:
        if isinstance(first_operand, str) and isinstance(second_operand, str):
            return first_operand.startswith(second_operand)
        return Filter.raise_type_error("startswith", first_operand, second_operand)

    @staticmethod
    def in_list(first_operand: Any, second_operand: Any) -> bool:
        if type(second_operand) in (list, set):
            return first_operand in second_operand
        return Filter.raise_type_error("in", first_operand, second_operand)

    @staticmethod
    def contains_string(first_operand: str, second_operand: str) -> bool:
        if isinstance(first_operand, str) and isinstance(second_operand, str):
            return second_operand in first_operand
        return Filter.raise_type_error("contains", first_operand, second_operand)

    @staticmethod
    def not_in_list(first_operand: Any, second_operand: Any) -> bool:
        if type(second_operand) in (list, set):
            return first_operand not in second_operand
        return Filter.raise_type_error("nin", first_operand, second_operand)

    @staticmethod
    def equal_to(first_operand: Any, second_operand: Any) -> bool:
        if isinstance(first_operand, type(second_operand)):
            return first_operand == second_operand
        return Filter.raise_type_error("==", first_operand, second_operand)

    @staticmethod
    def not_equal_to(first_operand: Any, second_operand: Any) -> bool:
        if isinstance(first_operand, type(second_operand)):
            return first_operand != second_operand
        return Filter.raise_type_error("!=", first_operand, second_operand)

    @staticmethod
    def less_than_or_equal_to(first_operand: Any, second_operand: Any) -> bool:
        if isinstance(first_operand, type(second_operand)):
            return first_operand <= second_operand
        return Filter.raise_type_error("<=", first_operand, second_operand)

    @staticmethod
    def greater_than_or_equal_to(first_operand: Any, second_operand: Any) -> bool:
        if isinstance(first_operand, type(second_operand)):
            return first_operand >= second_operand
        return Filter.raise_type_error(">=", first_operand, second_operand)

    def __init__(self, attribute: str, operator: str, value: Any):
        self.attribute = attribute
        self.operator = operator
        self.value = value

    def evaluate(self, obj: Dict[str, Any]) -> bool:
        # if not isinstance(obj, object):
        #     return False
        attr_value = getattr(obj, self.attribute)
        if self.operator is not None:
            if self.operator in self.op_funcs:
                return self.op_funcs[self.operator](attr_value, self.value)
            raise ValueError(f"'{self.operator}' is not a valid operator")
        if self.contains_regex(self.value):
            return re.match(self.value, attr_value)
        return attr_value == self.value

    def contains_regex(self, string):
        """
        Checks whether a string contains a regular expression.

        Args:
            s (str): The string to check.

        Returns:
            True if the string contains a regular expression, False otherwise.
        """
        try:
            re.compile(string)
        except (re.error, TypeError):
            return False
        return True

    @staticmethod
    def raise_type_error(
        operator: str, first_operand: Any, second_operand: Any
    ) -> None:
        """
        Raises a TypeError indicating that the given operands are not supported for a given operator.

        Args:
            op (str): The operator that caused the TypeError.
            x (Any): The first operand of the operator.
            y (Any): The second operand of the operator.

        Raises:
            TypeError: If the given operands are not supported for the given operator.
        """
        if operator in [">", ">=", "<", "<="]:
            raise TypeError(
                f"Invalid type for value of '{operator}' operator : expected int, found {type(second_operand).__name__}"
            )
        if operator in ["in", "nin"]:
            raise TypeError(
                f"Invalid type for value of '{operator}' operator : expected list, found {type(second_operand).__name__}"
            )
        if operator in ["contains", "startswith", "endswith"]:
            raise TypeError(f"'{operator}' lookup only works for string type fields")
        if operator in ["==", "!="]:
            raise TypeError(
                f"'{operator}' operator only works for same type fields, found {type(first_operand).__name__} and {type(second_operand).__name__}"
            )


class Query:
    """
    Représente une requête qui peut être évaluée sur un objet.

    Attributs:
    ----------
    filters : List[Union[Query, Filter]]
        Liste de filtres à appliquer à l'objet.

    Méthodes:
    ---------
    __and__(self, other) -> Query:
        Renvoie une nouvelle requête qui est la conjonction de cette requête et de la requête donnée.

    __or__(self, other) -> Query:
        Renvoie une nouvelle requête qui est la disjonction de cette requête et de la requête donnée.

    evaluate(self, obj) -> bool:
        Évalue cette requête sur l'objet donné et renvoie True si l'objet satisfait la requête, False sinon.
    """

    def __init__(self, filters: List[Union["Query", "Filter"]]) -> None:
        """
        Initialise une nouvelle requête avec les filtres donnés.

        Parameters:
        -----------
        filters : List[Union[Query, Filter]]
            Liste de filtres à appliquer à l'objet.
        """
        self.filters = filters

    def __and__(self, other: "Query") -> "Query":
        """
        Renvoie une nouvelle requête qui est la conjonction de cette requête et de la requête donnée.

        Parameters:
        -----------
        other : Query
            La requête à conjointe avec celle-ci.

        Returns:
        --------
        Query
            Une nouvelle requête qui est la conjonction de cette requête et de la requête donnée.
        """
        return Query(self.filters + other.filters)

    def __or__(self, other: "Query") -> "Query":
        """
        Renvoie une nouvelle requête qui est la disjonction de cette requête et de la requête donnée.

        Parameters:
        -----------
        other : Query
            La requête à disjoindre avec celle-ci.

        Returns:
        --------
        Query
            Une nouvelle requête qui est la disjonction de cette requête et de la requête donnée.
        """
        return Query([self, other])

    def evaluate(self, obj: Dict[str, Any]) -> bool:
        """
        Évalue cette requête sur l'objet donné et renvoie True si l'objet satisfait la requête, False sinon.

        Parameters:
        -----------
        obj : Any
            L'objet à évaluer.

        Returns:
        --------
        bool
            True si l'objet satisfait la requête, False sinon.
        """
        if isinstance(self.filters[0], Query):
            # opération OR
            return any(subquery.evaluate(obj) for subquery in self.filters)
            # opération AND
        return all(filter.evaluate(obj) for filter in self.filters)


class OrmCollection(ImprovedList):
    """
    A list-like collection class that extends ImprovedList and that implements an ORM overlay (wrapper) for a list of objects,
    providing an interface and additional methods for querying and manipulating objects in the list.
    """

    # def __repr__(self):
    #     """Provide a string representation of the OrmCollection instance."""
    #     items_repr = ", ".join([repr(item) for item in self])
    #     return f"OrmCollection([{items_repr}])"

    def where(self, *queries, **filters) -> "OrmCollection":
        """
        Filters the collection to only include objects that match the provided criteria.

        Args:
            *queries (Query): Query objects that are combined using the OR operator.
            **filters (dict): Key-value pairs of field names and values to filter by.
                Valid operators include "lt", "gt", "lte", "gte", "endswith", "startswith", "in", "nin", "contains".
                If an invalid operator is used, a ValueError is raised.

        Returns:
            OrmCollection: A new OrmCollection containing only objects where at least one of the given attributes matches.

        Raises:
            ValueError: If an invalid operator is used.
        """

        filters_list = []

        for query in queries:
            for filter_ in query.filters:
                filters_list.append(filter_)

        for key, value in filters.items():
            if "__" in key:
                attribute, operator = key.split("__")
                if operator not in Filter.op_funcs:
                    raise ValueError(f"'{operator}' is not a valid operator")
                filters_list.append(Filter(attribute, operator, value))
            else:
                filters_list.append(Filter(key, None, value))

        if not filters_list:
            return self.__class__()

        results = self.__class__()

        for elm in self:
            if any(query.evaluate(elm) for query in queries) or all(
                filt.evaluate(elm) for filt in filters_list
            ):
                results.append(elm)

        return results

    def find_by(self, **kwargs) -> object:
        """
        Finds a single object in the collection that matches the provided criteria. Raises an exception if no or more than
        one object is found.

        Args:
            **kwargs: Key-value (Dictionary) of field names and values to filter by.

        Returns:
            The first object in the OrmCollection where all given attributes match.

        Raises:
            BaseNotFound: If no objects are found that match the given attributes.
            BaseMultipleFound: If more than one object is found that matches the given attributes.
        """
        matching_objs = self.where(**kwargs)
        if len(matching_objs) == 0:
            raise BaseNotFound(f"No {self.__class__.__name__} found for {kwargs}")
        if len(matching_objs) > 1:
            raise BaseMultipleFound(
                f"More than one {self.__class__.__name__} found for {kwargs}"
            )
        return matching_objs.first()

    def order_by(self, key=None, reverse=False):
        """
        Sort the objects in the collection based on a field or a custom function.

        Args:
            key (str or function, optional): Field name or function to sort by. Defaults to None.
            reverse (bool, optional): True to sort in descending order, False to sort in ascending order. Defaults to False.

        Returns:
            A new OrmCollection containing the sorted objects.

        Raises:
            ValueError: If key is None and not all elements in the list are integers or floats.
            TypeError: If key is not a valid attribute name or function.
        """
        if not key:
            if all(isinstance(item, (int, float)) for item in self):
                return self.__class__(sorted(self))
            if all(isinstance(item, str) for item in self):
                return self.__class__(sorted(self, key=len))
            raise ValueError("All elements in the list must be integers or floats.")
        if isinstance(key, str):
            return self.__class__(
                sorted(
                    self,
                    key=lambda x: getattr(x, key),
                    reverse=reverse,
                )
            )
        if callable(key):
            return self.__class__(sorted(self, key=key, reverse=reverse))
        raise TypeError("key must be a string attribute name or a function")

    def group_by(self, key_func):
        """
        Group the objects in the collection based on a given function.

        Args:
            key_func (function): A function that takes an object as input and returns the group key.

        Returns:
            A dictionary where the keys are the return values of the key function and
            the values are OrmCollections containing the corresponding objects.

        Raises:
            N/A
        """
        groups = {}
        for obj in self:
            key = key_func(obj)
            if key not in groups:
                groups[key] = OrmCollection()
            groups[key].append(obj)
        return groups

    def limit(self, count):
        """
        Return a new OrmCollection with the first n objects in the collection.

        Args:
            count (int): The number of objects to include in the new collection.

        Returns:
            A new OrmCollection containing the first n objects in the collection.

        Raises:
            N/A
        """
        return self.__class__(self[:count])

    def offset(self, count):
        """
        Return a new OrmCollection with the objects after the first n objects in the collection.

        Args:
            count (int): The number of objects to skip.

        Returns:
            A new OrmCollection containing the objects after the first n objects in the collection.

        Raises:
            N/A
        """
        return self.__class__(self[count:])

    def all(self):
        """
        Return a new OrmCollection containing all objects in the collection.

        Args:
            N/A

        Returns:
            A new OrmCollection containing all objects in the collection.

        Raises:
            N/A
        """
        return self.__class__(self)

    def _check_simple_type(self, lst):
        """
        Check if all items in the given list are of simple types.

        Args:
            lst (list): The list to check.

        Returns:
            bool: True if all items in the list are of simple types (int, float, or str), False otherwise.

        Raises:
            N/A
        """
        return all(isinstance(item, (int, float, str)) for item in lst)

    def distinct(self, *args):
        """
        Return a new OrmCollection containing only the unique objects in the collection
        based on one or more attributes.

        Args:
            *args (str): One or more attribute names to use for finding unique objects.

        Returns:
            A new OrmCollection containing only the unique objects in the collection.

        Raises:
            ValueError: If no arguments are provided or if at least one argument is not a field.
            AttributeError: If at least one argument is not an attribute of the objects in the collection.
        """

        # If no args are provided, return a new collection with unique elements
        if not args and self._check_simple_type(self):
            return self.__class__(list(OrderedDict.fromkeys(self)))
        if not args and not self._check_simple_type(self):
            raise ValueError("At least one field must be provided")

        # for field in args:
        #     if not hasattr(self[0], field):
        #         raise AttributeError(
        #             f"Le champ '{field}' n'existe pas dans la classe {self[0].__class__.__name__}."
        #         )

        distinct_values = []
        seen = set()
        for elm in self:
            # distinct_values.append(tuple(getattr(elm, field) for field in args))
            values = tuple(getattr(elm, field) for field in args)
            if values not in seen:
                seen.add(values)
                distinct_values.append(elm)

        # return self.__class__(list(dict.fromkeys(distinct_values)))
        return self.__class__(distinct_values)
