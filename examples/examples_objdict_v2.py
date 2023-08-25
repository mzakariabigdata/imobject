# Importer la classe ObjDict
from imobject import ObjDict, ImprovedList
import pytest


def test_objdict_advanced():
    # Adding your code with assertions:
    app = ObjDict()
    app.account = {}
    assert isinstance(app.account, ObjDict)

    app.account.unsername = "John"
    assert app.account.unsername == "John"

    app.account.password = "1234"
    assert app.account.password == "1234"

    app.account.token = "1234567890"
    assert app.account.token == "1234567890"

    app.account.test = {}
    assert isinstance(app.account.test, ObjDict)

    app.account.test.name = "test"
    assert app.account.test.name == "test"

    app.account.test.age = 33
    assert app.account.test.age == 33

    app.account.test2 = {}
    assert isinstance(app.account.test2, ObjDict)

    app.account.test2.name = "test value 2"
    assert app.account.test2.name == "test value 2"

    app.account.test2.age = 34
    assert app.account.test2.age == 34

    del app.account.test2.name
    with pytest.raises(AttributeError):
        _ = app.account.test2.name

    app.account.users = []
    assert isinstance(app.account.users, ImprovedList)

    app.account.users.append({"name": "John", "age": 25})
    assert app.account.users[0].name == "John"

    app.account.users.append({"name": "Alice", "age": 30})
    assert app.account.users[1].name == "Alice"

    app.account.users[0].name = "zakaria"
    assert app.account.users[0].name == "zakaria"

    app.account.users[0].age = 33
    assert app.account.users[0].age == 33
    app.account.users[1].name = "zakaria"
    assert app.account.users[1].name == "zakaria"

    app.account.some_string = "Hello"
    assert app.account.some_string == "Hello"

    with pytest.raises(AttributeError):
        _ = app.account.non_existent_attribute

    app.account.update({"new_key": "new_value"})
    assert app.account.new_key == "new_value"

    regular_dict = app.to_dict()
    assert isinstance(regular_dict, dict)
    assert regular_dict["account"]["unsername"] == "John"

    app.deef = "test"
    assert app["deef"] == "test"

    app.nested = {"inner": {"key": "value"}}
    assert isinstance(app.nested.inner, ObjDict)
    assert app.nested.inner.key == "value"

    del app.account.users[0].name
    with pytest.raises(AttributeError):
        _ = app.account.users[0].name


test_objdict_advanced()
