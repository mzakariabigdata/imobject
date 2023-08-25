import subprocess
import os

examples = [
    # "examples_improved_list.py",
    # "examples_objdict.py",
    # "examples_orm_collection.py",
    # "examples_ioc.py",
    "examples_objdict_v2.py",
]

os.chdir(".")

for example in examples:
    print(f"\nExécution de {example} :")
    result = subprocess.run(["python", example], capture_output=True, text=True)
    print(result.stdout)
