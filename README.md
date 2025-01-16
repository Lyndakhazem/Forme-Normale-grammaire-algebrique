# Transformation de Grammaires Algébriques

## Description du projet
**Projet L3 INFORMATIQUE 2024/2025 (COMPILATION)**

Ce projet permet de **lire une grammaire algébrique** depuis un fichier et de la transformer dans les **formes normales de Greibach** et **de Chomsky** en fichiers de sortie. Puis a partir de ces formes transformées, il génère tous les mots dont la longueur est inférieure à une longueur donnée 'n'.  

### Fonctionnalités principales :
1. Lecture d'une grammaire algébrique depuis un fichier d'entrée.  
2. Transformation de la grammaire en :  
   - Forme normale de **Greibach**.  
   - Forme normale de **Chomsky**.  
3. Génération des mots possibles respectant une longueur maximale donnée pour chaque forme transformée.  

---
## Définitions des formes normales

### 1. Généralités
Une **forme normale** est une manière standardisée de représenter une grammaire. Ces formes permettent de simplifier l'analyse et la manipulation des grammaires, en particulier dans le cadre des langages formels.

### 2. Forme normale de Greibach
Une grammaire algébrique est sous **forme normale de Greibach** si toutes les règles sont de la forme :
-  X → aA1A2...An avec  n ≥ 1  
-  X → a 
- S → ε seulement si ε appartient au langage.
  

Ici :  
- \( X \) représente un **non-terminal**,  
- \( a \) représente un **terminal**,  
- \( A1, A2, ..., An \) représentent des non-terminaux.  

### 3. Forme normale de Chomsky
Une grammaire algébrique est sous **forme normale de Chomsky** si toutes les règles sont de la forme :
-  X → YZ où \( Y \) et \( Z \) sont des non-terminaux,  
-  X → a où \( a \) est un terminal,  
-  S → ε seulement si ε appartient au langage. 

 

---


## Conventions utilisées

### 1. **Ensemble des terminaux**  
L'ensemble des **terminaux** est constitué des **26 lettres minuscules** de l'alphabet (a, b, c, ... z).  

### 2. **Symbole ε (epsilon)**  
Le symbole **`E`** majuscule représente **ε** (mot vide).  

### 3. **Non-terminaux**  
Les **non-terminaux** sont représentés par une des **25 lettres majuscules** (sauf `E`), suivie d’un chiffre compris entre **0 et 9**.  
Par exemple : `T8`, `A5`, `R0`. Il y a donc **250 non-terminaux possibles**.  

### 4. **Format du fichier d'entrée**  
- Chaque ligne du fichier d’entrée représente une **règle** de la grammaire sous la forme suivante :  
    membre_gauche : membre_droit.
- Le **membre_gauche** de la **première règle** du fichier est considéré comme l’**axiome** de la grammaire.  
- Exemple d’un fichier valide :
```plaintext
    S0 : aT1
    T1 : bT2
    T2 : a
    T2 : E
```

### 5. **Démo en CLI avec un exemple sur un fichier test.general**
```plaintext
    cd src
```
- Générer deux fichiers nom_fichier.chomsky et nom_fichier.greibach
```plaintext
    python grammaire.py nom_fichier.general
```
- Générer le fichier nom_fichier_N_chomsky.res
```plaintext
    python generer.py <N = LongueurMaxMot> nom_fichier.chomsky > test_N_chomsky.res
```
- Générer le fichier nom_fichier_N_greibach.res
```plaintext
    python generer.py <N = LongueurMaxMot> nom_fichier.greibach > test_N_greibach.res
```
- Exemple :
```plaintext
    cd src
    python grammaire.py test.general
    python generer.py 4 test.chomsky > test_4_chomsky.res
    python generer.py 4 test.greibach > test_4_greibach.res
```
### 6. **Démo avec Makefile**
```plaintext
    cd src
```
- Exécuter make qui génére les résultats pour tous les fichiers
```plaintext
    make
```
- Ou exécuter make nom_fichier qui génére uniquement les résultats pour le fichier nom_fichier.general
```plaintext
    make nom_fichier
```
- Exécuter make clean pour supprimer tous les fichiers générés
```plaintext 
    make clean
```
```plaintext
    cd src
    make test
```
---

## Auteurs :

Projet est fait en binome , constitué de **Massinissa MACHTER** [https://github.com/machterMassi06] et **Lynda KHAZEM** [https://github.com/Lyndakhazem].

