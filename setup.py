from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="imobject",
    version="1.0.6",
    author="Zakaria Morchid",
    author_email="morchid.zakariaa@gmail.com",
    description="Imporve object",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mzakariabigdata/imobject",
    project_urls={
        "Bug Tracker": "https://github.com/mzakariabigdata/imobject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
)
