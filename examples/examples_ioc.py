from imobject import ObjectFactory


class Parent:
    def __init__(self, name):
        self.name = name

    # def __repr__(self):
    #     return f"Parent(name={self.name}, child1={self.child1}, child2={self.child2})"


class Child:
    def __init__(self, age):
        self.age = age

    def __repr__(self):
        return f"Child(age={self.age})"


class Child:
    def __init__(self, age):
        self.age = age

    def __repr__(self):
        return f"Child(age={self.age})"


class Children:
    def __init__(self, age):
        self.age = age

    def __repr__(self):
        return f"children(age={self.age})"


# Configuration pour créer une instance de Parent avec des instances de Child en attributs
conf = {
    "class": "parent",
    "params": {"name": "Parent1"},
    "child": {"class": "child", "params": {"age": 5}},
    "children": [
        {"class": "child", "params": {"age": 6}},
        {"class": "child", "params": {"age": 7}},
    ],
}

# Correspondance entre les types de classes et les classes réelles
class_map = {
    "parent": Parent,
    "child": Child,
    "children": Children,
}

# Création d'une instance de ObjectFactory et utilisation pour créer un objet à partir de la configuration
factory = ObjectFactory(conf, class_map)
parent_obj = factory.get_object()

print(parent_obj.child)
# Affichage de l'objet créé
print(parent_obj.__dict__)
