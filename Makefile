###################
##### include #####
###################
# Inclusion du fichier de fonctions
include Makefile-Functions.mk

###################
### Virtual ENV ###
###################
env-create: ## Crée un environnement virtuel "pattern" utilisant Python 3.11 avec conda.
	@echo "Creation de l'environnement virtuel \"pattern\" utilisant Python 3.11 avec conda..."
	conda create -n pattern python=3.11

env-delete: ## Supprime l'environnement virtuel "pattern" créé précédemment avec conda.
	@echo "Suppression l'environnement virtuel \"pattern\"..."
	conda env remove -n pattern

env-variables: ## Ajouter costums variables au Shell
	@echo "Ajout des variables d'environnement personnalisées au Shell..."
	. ./.env.sh

get-vscode-extensions: ## Récupérer la liste des extensions installées dans VS Code
	@echo "Récupération de la liste des extensions installées dans VS Code..."
	code --list-extensions >> vscode-extensions.txt

install-vscode-extensions: vscode-extensions.txt ## Installe les extensions VS Code à partir du fichier vscode-extensions.txt.
	@echo "Installation des extensions VS Code à partir vscode-extensions.txt..."
	cat vscode-extensions.txt | xargs -n 1 code --install-extension

env-init: ## Installe l'outil pipenv dans l'environnement système.
	@echo "Installation l'outil pipenv..."
	pip install pipenv

env-activate: ## Active l'environnement virtuel "pattern" créé précédemment et définit la variable PYTHONPATH pour qu'elle pointe vers le répertoire de travail courant.
	@echo "Activation l'environnement virtuel \"pattern\"..."
	source ~/anaconda3/etc/profile.d/conda.sh; conda activate pattern
	export PYTHONPATH=$(pwd)/src

requirements-lock: ## Verrouille les dépendances de production dans un fichier Pipfile.lock à partir du fichier Pipfile.
	@echo "Verrouillage des dépendances de production dans  Pipfile.lock..."
	pipenv lock

requirements-prod: requirements-lock Pipfile ## Génère un fichier requirements-prod.txt contenant une liste des dépendances de production et de leur hachage à partir du fichier Pipfile.lock.
	@echo "Génération de requirements-prod.txt à partir Pipfile.lock..."
	pipenv requirements --hash > requirements-prod.txt

requirements-dev: env-init requirements-lock Pipfile ##  Génère un fichier requirements-dev.txt contenant une liste des dépendances de développement et de leur hachage à partir du fichier Pipfile.lock.
	@echo "Génération de requirements-dev.txt à partir Pipfile.lock..."
	pipenv requirements --hash --dev > requirements-dev.txt

install-requirements-prod: requirements-prod ##  Installe les dépendances de production en utilisant le fichier requirements-prod.txt.
	@echo "Installer les dépendances de production en utilisant le fichier requirements-prod.txt."
	pip3 install -r requirements-prod.txt

install-requirements-dev: requirements-dev ## Installe les dépendances de développement en utilisant le fichier requirements-dev.txt.
	@echo "Installer les dépendances de développement en utilisant le fichier requirements-dev.txt."
	pip3 install -r requirements-dev.txt

install-auto-completion: ## Install auto-completion (in alpine)
	@apk add --no-cache  bash-completion > /dev/null 2>&1
	@echo "source /etc/profile.d/bash_completion.sh" >> ~/.bashrc
	@echo -e "\033[31mTap this command to activate auto-completion:\033[0m \033[32msource ~/.bashrc\033[0m"
	
.PHONY: env-activate env-create kivy-install env-init requirements-prod requirements-dev install-requirements-prod install-requirements-dev requirements-lock get-vscode-extensions install-vscode-extensions env-variables install-auto-completion

###################
###### Behave ######
###################
behave: ## Exécuter les tests comportementaux en utilisant l'outil Behave.
	@echo "Lancement des tests comportementaux en utilisant l'outil Behave..."
	behave --no-capture
###################
###### Build ######
###################
app-examples: ## Lancer les exemples de l'application.
	@echo "Lancement des exemples de l'application..."
	@cd examples && python run_examples.py
app-clean: ## Nettoie les fichiers générés précédemment pour l'application.
	@echo "Nettoyage des fichiers générés par dist..."
	rm -f dist/*.gz
app-dist: app-clean  ## Crée une distribution de l'application.
	@echo "Création d'une distribution de l'application..."
	python setup.py sdist
app-deploy: app-dist ## Déploie l'application en envoyant la distribution sur PyPI.
	@echo "Déploiement d'une distribution de l'application sur PyPI."
	twine upload dist/*
app-install: ## Installer 'imobject' localement
	@echo "Installation de 'imobject' localement..."
	pip install -e .
app: src/app.py  ## Lance l'application principale en exécutant le fichier src/app.py.
	@echo "Lancement de l'application principale en exécutant le fichier src/app.py..."
	pyclean . -q
	cd src && python app.py
	pyclean . -q
format: ## Formate le code source en utilisant l'outil Black.
	@echo "Formatage du code source..."
	@python -m black .
format-check: ## Formate check en utilisant l'outil Black.
	python -m black . --check
lint: ## Vérifier le code source avec pylint.
	@echo "Vérification du code source avec pylint..."
	@python -m pylint src/. tests/.
	@echo "Vérification terminée."

tests: clean-py ## Exécute les tests unitaires en utilisant l'outil pytest.
	@echo "Exécution des tests unitaires..."
	@python -m pytest -s -vv
	@echo "Exécution terminée."

cov: ## Exécute les tests unitaires et génère un rapport de couverture de code en HTML dans le dossier reports/.
	@echo "Exécution des tests unitaires avec covergae HTML..."
	@python -m pytest -s -vvv --cov-report term-missing:skip-covered --cov-report=html:reports/ --cov=src/imobject tests/

cov-xml: ## Exécute les tests unitaires et génère un rapport de couverture de code au format XML dans le dossier reports/.
	@echo "Exécution des tests unitaires avec covergae XML..."
	@python -m pytest  -rX -vvv --cov-report term-missing:skip-covered --cov-report=xml:reports/coverage.xml --cov=src/imobject tests/

clean-py: ## Nettoie les fichiers générés précédemment en utilisant l'outil pyclean.
	@echo "Nettoyage des fichiers cachés..."
	pyclean . -q
fl: format lint ## Formatage et vérification de code.
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

docs-init: ## Initialisation du repo docs.
	@echo "Initialisation du repo docs..."
	$(call create-dir, $(DOCSDIR)) && cd docs && $(SPHINXINIT) && sphinx-apidoc -o docs src/
	@echo "Initialisation terminée."

docs: clean-docs ## Génération de la documentation avec Sphinx.
	@echo "Génération de la documentation avec Sphinx..."
	$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	# cd docs && make html
	@echo "Génération terminée."

clean-docs: ## Suppression des fichiers générés pour la documentation.
	@echo "Suppression des fichiers générés pour la documentation..."
	rm -rf "$(BUILDDIR)"
	@echo "Nettoyage terminé."

##########################
###### Change logs #######
##########################

pre-commit-install: ## Installation des hooks pre-commit.
	@echo "Installation des hooks pre-commit..."
	pre-commit install
	@echo "Installation terminée."

pre-commit-run: ## Exécution des hooks pre-commit sur tous les fichiers.
	@echo "Exécution des hooks pre-commit sur tous les fichiers..."
	pre-commit run --all-files
	@echo "Exécution terminée."

.PHONY: pre-commit-install pre-commit-run

##########################
###### Change logs #######
##########################

DOCSDIR			:= 2.0.0

add-fragments: ## Création de nouveaux fragments de changelog.
	@echo "Création de nouveaux fragments de changelog..."
	towncrier create --config towncrier.toml --content 'Can also be ``rst`` as well!' 3452.doc.rst
	@echo "Création terminée."

newsfragment: ## Génère les fichiers .rst pour chaque section de changelog
	@echo "Génération des fichiers .rst pour chaque section de changelog..."
	towncrier --draft --yes
	@echo "Génération terminée."


build-news: ## Génère les fichiers de sortie pour les nouvelles sections de changelog
	@echo "Génération des fichiers de sortie pour les nouvelles sections de changelog..."
	towncrier --yes
	@echo "Génération terminée."

costum-changelogs: ## Génération des journaux de changement personnalisés.
	@echo "Génération des journaux de changement personnalisés..."
	cd changelogs/costum && python changelogs.py
	@echo "Génération terminée."

.PHONY: newsfragment add-fragments build-news costum-changelogs


##########################
########## Help ##########
##########################

.PHONY: help kaka
help: ## Affiche cette aide
	@echo "Les commandes disponibles sont :"
	@echo ""
	@grep -E '^[a-zA-Z0-9_-]+:.*?# .*$$' Makefile | sort | awk -F':.*?# ' '/^[a-zA-Z0-9_-]+:.*?#/ {printf "  make \033[36m%-16s\033[0m %s\n", $$1, $$2}'

help2: ## Affiche cette aide
	@echo "Voici les commandes disponibles :"
	@echo ""
	@awk -F ':.*?##' '/^[^\t].+?:.*?##/ { printf " make \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST) | sort
