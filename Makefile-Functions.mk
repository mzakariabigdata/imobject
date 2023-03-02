# Définition de la fonction create-dir; vérifier l'existence d'un dossier et le créer s'il n'existe pas:
define create-dir
	if [ ! -d $(1) ]; then mkdir -p $(1); fi
endef
