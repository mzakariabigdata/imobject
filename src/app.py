""" App module"""


from imobject import OrmCollection, ObjDict, ImprovedList, Query, Filter


def main3():
    # from datetime import datetime
    # from typing import List

    # class MyClass:
    #     def __init__(self, name: str, date: str):
    #         self.name = name
    #         self.date = datetime.strptime(date, "%Y-%m-%d")

    # def compare_by_date(a: MyClass, b: MyClass) -> int:
    #     if a.date < b.date:
    #         return -1
    #     elif a.date > b.date:
    #         return 1
    #     else:
    #         return 0

    # # Créer une liste d'objets MyClass non triée
    # objects = ImprovedList(
    #     [
    #         MyClass("Obj1", "2022-01-05"),
    #         MyClass("Obj2", "2022-02-03"),
    #         MyClass("Obj2", "2022-02-03"),
    #         MyClass("Obj2", "2022-02-03"),
    #         MyClass("Obj3", "2021-12-25"),
    #         MyClass("Obj4", "2022-01-20"),
    #     ]
    # )

    # # Trier la liste d'objets MyClass par date en utilisant la fonction compare_by_date
    # sorted_objects = objects.map(
    #     called=".date",
    #     filter_func=None,
    #     max_elements=None,
    #     reverse_order=False,
    #     sort_func=compare_by_date,
    #     return_type="ImprovedList",
    # )

    # # Afficher le résultat trié
    # for obj in sorted_objects:
    #     print(f"{obj.name} - {obj.date}")

    my_list = ImprovedList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    result = my_list.map(lambda x: x**2, max_elements=3, reverse_order=False)
    print(result)


if __name__ == "__main__":
    # main()
    # main2()
    main3()
