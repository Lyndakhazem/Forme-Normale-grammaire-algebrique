# executables et variables
GRAMMAIRE = grammaire.py
GENERER = generer.py
LENGTH = 4

# Recherche automatiquement tous les fichiers .general dans le répertoire
TEST_FILES = $(wildcard *.general)

# Règle principale : traite tous les fichiers .general dans le repertoire
all: $(basename $(TEST_FILES))

# Règles spécifiques pour chaque fichier .general
# Exemple : 'make test' --> traite uniquement test.general
$(basename $(TEST_FILES)): %: %.general
	@echo "Processing $<..."
	python3 $(GRAMMAIRE) $<  
	python3 $(GENERER) $(LENGTH) $(basename $<).chomsky > $(basename $<)_$(LENGTH)_chomsky.res
	python3 $(GENERER) $(LENGTH) $(basename $<).greibach > $(basename $<)_$(LENGTH)_greibach.res
	diff $(basename $<)_$(LENGTH)_chomsky.res $(basename $<)_$(LENGTH)_greibach.res 

# Nettoyage des fichiers générés
clean:
	rm -f *.chomsky *.greibach *_$(LENGTH)_chomsky.res *_$(LENGTH)_greibach.res
