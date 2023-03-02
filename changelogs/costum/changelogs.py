import yaml
from yaml.loader import SafeLoader
from jinja2 import Environment, FileSystemLoader

# Open the file and load the file
with open("1.0.0.yml") as f:
    docs = yaml.load_all(f, yaml.FullLoader)

    # for doc in docs:
    #     print(doc)
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("towncrier.j2")
    output = template.render(
        # project_name="MyProject",
        fragments=docs,
    )

    print(output)
