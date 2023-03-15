"""This module provides an ObjectFactory class for creating objects based on a configuration file.

Classes:
- ObjectFactory: A factory class for creating objects based on a configuration file.

"""


class ObjectFactory:
    """Factory class to create objects based on configuration dictionary.

    This class provides a method for creating objects based on configuration
    dictionaries. It uses a class map to map class names to class objects.

    Attributes:
        conf (dict): A dictionary representing the configuration of the object to create.
        class_map (dict): A dictionary mapping class names to class objects.

    Methods:
        get_object: Create an object based on the configuration passed to the constructor.
        create_object: Create an object based on a configuration dictionary.

    Raises:
        ValueError: If the class type in the configuration dictionary is not found in the class map.

    Example:
        To create an object using the `ObjectFactory` class:

        >>> conf = {'class': 'MyClass', 'params': {'foo': 'bar'}}
        >>> class_map = {'MyClass': MyClass}
        >>> factory = ObjectFactory(conf, class_map)
        >>> obj = factory.get_object()
    """

    def __init__(self, conf: dict, class_map: dict):
        """
        Initialise une instance de ObjectFactory avec un dictionnaire de configuration
        et un mapping de classes.

        Args:
        - conf (dict): Un dictionnaire de configuration contenant des informations sur
                        les objets à créer.  Il doit inclure le type de classe
                        (sous forme de chaîne de caractères) et éventuellement des paramètres
                          de construction et des attributs pour les objets imbriqués.
        - class_map (dict): Un dictionnaire de correspondance de types de classe,
                            qui associe les noms des types de classe (sous forme de chaîne 
                            de caractères) aux classes réelles (objets Python).

        Returns:
        - None
        """
        self.class_map = class_map
        self.conf = conf

    def get_object(self):
        """
        Crée un objet à partir de la configuration stockée dans l'instance.

        Args:
        - None

        Returns:
        - obj : L'objet créé à partir de la configuration stockée dans l'instance.
        """
        return self.create_object(self.conf)

    def _create_dynamic_class(self, class_name):
        """
        Crée une classe dynamique en fonction de la classe donnée.

        :param class_name: La classe à partir de laquelle la classe dynamique sera créée.
        :return: La classe dynamique créée.
        """

        # Création d'une nouvelle classe héritant de la classe initiale
        # Cette ligne crée un nom de classe pour la nouvelle classe dynamique
        # en préfixant le nom de la classe initiale avec "Dynamic". Par exemple,
        # si la classe initiale s'appelle "Parent", la nouvelle classe dynamique
        # s'appellera "DynamicParent". Cela permet de différencier facilement
        # la classe initiale de la nouvelle classe dynamique.
        dynamic_class_name = f"Dynamic{class_name.__name__}"
        # Cette ligne crée une nouvelle classe dynamique en utilisant la fonction type().
        # La fonction type() est utilisée pour créer de nouvelles classes à la volée.
        # Elle prend trois arguments :
        #  - Le nom de la classe (ici, dynamic_class_name)
        #  - Un tuple contenant les classes de base (superclasses) à partir desquelles
        #    la nouvelle classe doit hériter (ici, (class_name,) - la nouvelle classe hérite
        #    de la classe initiale)
        #  - Un dictionnaire contenant les attributs et méthodes de la nouvelle classe
        #    (ici, {} - initialement vide, car nous allons ajouter des propriétés dynamiquement)
        dynamic_class = type(dynamic_class_name, (class_name,), {})
        return dynamic_class

    def _set_list_property(self, obj, dynamic_class, key, value):
        """
        Attribue une liste d'objets à une propriété de l'objet donné.

        :param obj: L'objet auquel attribuer la liste d'objets.
        :param dynamic_class: La classe dynamique de l'objet.
        :param key: Le nom de la propriété.
        :param value: La liste des objets à attribuer.
        """
        setattr(obj, f"_{key}", [])
        for item in value:
            child_obj = self.create_object(item)
            getattr(obj, f"_{key}").append(child_obj)
            print(f"{obj.__class__.__name__}.{key} = {child_obj.__class__.__name__}")

        self._create_dynamic_property(dynamic_class, key)

    def _set_single_property(self, obj, dynamic_class, key, value):
        """
        Attribue un objet unique à une propriété de l'objet donné.

        :param obj: L'objet auquel attribuer l'objet unique.
        :param dynamic_class: La classe dynamique de l'objet.
        :param key: Le nom de la propriété.
        :param value: L'objet à attribuer.
        """
        child_obj = self.create_object(value)
        setattr(obj, f"_{key}", child_obj)
        print(f"{obj.__class__.__name__}.{key} = {child_obj.__class__.__name__}")
        self._create_dynamic_property(dynamic_class, key)

    def _create_dynamic_property(self, dynamic_class, attr_name):
        """
        Crée une propriété dynamique pour la classe donnée.

        :param dynamic_class: La classe pour laquelle créer la propriété dynamique.
        :param attr_name: Le nom de l'attribut pour lequel créer la propriété.
        """

        def create_getter(attr_name):
            def getter(self):
                return getattr(self, f"_{attr_name}")

            return getter

        def create_setter(attr_name):
            def setter(self, value):
                setattr(self, f"_{attr_name}", value)

            return setter

        setattr(
            dynamic_class,
            attr_name,
            property(create_getter(attr_name), create_setter(attr_name)),
        )

    def create_object(self, conf: dict):
        """
        Crée un objet à partir d'un dictionnaire de configuration.

        Args:
        - conf (dict): Un dictionnaire de configuration contenant des
                        informations sur l'objet à créer.

        Returns:
        - obj : L'objet créé à partir du dictionnaire de configuration.
        """
        class_type = conf.get("class")
        class_name = self.class_map.get(class_type)
        if class_name is None:
            raise ValueError(f"Class type {class_type} not found in class map")

        dynamic_class = self._create_dynamic_class(class_name)

        # Instanciation de la nouvelle classe
        obj = dynamic_class(**conf.get("params", {}))
        print(f"{obj.__class__.__name__}()")

        for key, value in conf.items():
            if key in ["class", "params"]:
                continue
            if isinstance(value, list):
                self._set_list_property(obj, dynamic_class, key, value)
            else:
                self._set_single_property(obj, dynamic_class, key, value)

        return obj
