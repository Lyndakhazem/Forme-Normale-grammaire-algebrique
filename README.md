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
- \( X \to aA_1A_2...A_n \) avec \( n \geq 1 \)  
- \( X \to a \)  
- \( S \to \varepsilon \) uniquement si \( \varepsilon \) appartient au langage.  

Ici :  
- \( X \) représente un **non-terminal**,  
- \( a \) représente un **terminal**,  
- \( A_1, A_2, ..., A_n \) représentent des non-terminaux.  

### 3. Forme normale de Chomsky
Une grammaire algébrique est sous **forme normale de Chomsky** si toutes les règles sont de la forme :
- \( X \to Y Z \) où \( Y \) et \( Z \) sont des non-terminaux,  
- \( X \to a \) où \( a \) est un terminal,  
- \( S \to \varepsilon \) uniquement si \( \varepsilon \) appartient au langage.  

La forme normale de Chomsky est particulièrement utile pour les algorithmes comme celui de l’analyse syntaxique CYK (Cocke–Younger–Kasami).  

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
---

## Auteurs :

Projet est fait en binome , constitué de **Massinissa MACHTER** [https://github.com/machterMassi06] et **Lynda KHAZEM** [https://github.com/Lyndakhazem].

