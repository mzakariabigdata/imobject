###################
##### include #####
###################
# Inclusion du fichier de fonctions
include Makefile-Functions.mk

###################
### Virtual ENV ###
###################
# Crée un environnement virtuel "pattern" utilisant Python 3.11 avec conda.
env-create:
	conda create -n pattern python=3.11
# Supprime l'environnement virtuel "pattern" créé précédemment avec conda.
env-delete:
	conda env remove -n pattern
# Ajouter costums variables au Shell
env-variables:
	. ./.env.sh
# Récupérer la liste des extensions installées dans VS Code
get-vscode-extensions:
	code --list-extensions >> vscode-extensions.txt
# Installe les extensions VS Code à partir du fichier vscode-extensions.txt.
install-vscode-extensions: vscode-extensions.txt
	cat vscode-extensions.txt | xargs -n 1 code --install-extension
# Installe l'outil pipenv dans l'environnement système.
env-init:
	pip install pipenv
# Active l'environnement virtuel "pattern" créé précédemment et définit la variable PYTHONPATH pour qu'elle pointe vers le répertoire de travail courant.
env-activate:
	source ~/anaconda3/etc/profile.d/conda.sh; conda activate pattern
	export PYTHONPATH=$(pwd)/src
# Verrouille les dépendances de production dans un fichier Pipfile.lock à partir du fichier Pipfile.
requirements-lock:
	pipenv lock
# Génère un fichier requirements-prod.txt contenant une liste des dépendances de production et de leur hachage à partir du fichier Pipfile.lock.
requirements-prod: requirements-lock Pipfile
	pipenv requirements --hash > requirements-prod.txt
#  Génère un fichier requirements-dev.txt contenant une liste des dépendances de développement et de leur hachage à partir du fichier Pipfile.lock.
requirements-dev: env-init requirements-lock Pipfile
	pipenv requirements --hash --dev > requirements-dev.txt
#  Installe les dépendances de production en utilisant le fichier requirements-prod.txt.
install-requirements-prod: requirements-prod
	pip3 install -r requirements-prod.txt
# Installe les dépendances de développement en utilisant le fichier requirements-dev.txt.
install-requirements-dev: requirements-dev
	pip3 install -r requirements-dev.txt

.PHONY: env-activate env-create kivy-install env-init requirements-prod requirements-dev install-requirements-prod install-requirements-dev requirements-lock get-vscode-extensions install-vscode-extensions env-variables

###################
###### Build ######
###################
app-examples:
	cd examples && python examples_improved_list.py
	cd examples && python examples_objdict.py
	cd examples && python examples_orm_collection.py
	cd examples && python examples_ioc.py
app-clean:
	rm -f dist/*.gz
app-dist: app-clean
	python setup.py sdist
app-deploy: app-dist
	twine upload dist/*
app-install:
	pip install -e .
# Lance l'application principale en exécutant le fichier src/app.py.
app: src/app.py
	pyclean . -q
	cd src && python app.py
	pyclean . -q
# Formate le code source en utilisant l'outil Black.
format:
	python -m black .
format-check:
	python -m black . --check
# Vérifie le code source à l'aide de l'outil Pylint.
lint:
	python -m pylint src/. tests/.
# Exécute les tests unitaires en utilisant l'outil pytest.
tests: clean-py
	python -m pytest -s -vv
# Exécute les tests unitaires et génère un rapport de couverture de code en HTML dans le dossier reports/.
cov:
	python -m pytest -s -vvv --cov-report term-missing:skip-covered --cov-report=html:reports/ --cov=src/imobject tests/
# Exécute les tests unitaires et génère un rapport de couverture de code au format XML dans le dossier reports/.
cov-xml:
	python -m pytest  -rX -vvv --cov-report term-missing:skip-covered --cov-report=xml:reports/coverage.xml --cov=src/imobject tests/
# Nettoie les fichiers générés précédemment en utilisant l'outil pyclean.
clean-py:
	pyclean . -q
fl: format lint
.PHONY: tests clean-py lint format app app-clean fl app-examples

###################
###### Docs #######
###################
# Sphinx documentation
SPHINXOPTS		=
SPHINXINIT		= sphinx-quickstart
SPHINXBUILD		= sphinx-build
SOURCEDIR		= docs/source
BUILDDIR		= docs/build
DOCSDIR			= docs

.PHONY: docs-init docs clean-docs


docs-init:
	$(call create-dir, $(DOCSDIR)) && cd docs && $(SPHINXINIT) && sphinx-apidoc -o docs src/

docs: clean-docs
	$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	# cd docs && make html
clean-docs:
	rm -rf "$(BUILDDIR)"

##########################
###### Change logs #######
##########################

pre-commit-install:
	pre-commit install
pre-commit-run:
	pre-commit run --all-files

.PHONY: pre-commit-install pre-commit-run

##########################
###### Change logs #######
##########################

DOCSDIR			:= 2.0.0

add-fragments:
	towncrier create --config towncrier.toml --content 'Can also be ``rst`` as well!' 3452.doc.rst
# Génère les fichiers .rst pour chaque section de changelog
newsfragment:
	towncrier --draft --yes

# Génère les fichiers de sortie pour les nouvelles sections de changelog
build-news:
	towncrier --yes

costum-changelogs:
	cd changelogs/costum && python changelogs.py

.PHONY: newsfragment add-fragments build-news costum-changelogs
