import sys
from funct import lire 

def extraire_symboles_dans_mot(mot):
    '''
        Découpe un en symboles (terminaux et non-terminaux).
        Exemple : si mot ="aA1B2" sera découpé en ["a","A1", "B2"]
        Arguments:
            mot: La production à découper (chaîne de caractères).
        return Liste des symboles separer.
    '''
    symbols = []
    i = 0
    while i < len(mot):
        if mot[i].isupper() and i + 1 < len(mot) and mot[i+1].isdigit():  # Non-terminal
            symbols.append(mot[i:i+2])  
            i += 2  # On saute ces deux caractères
        else:
            symbols.append(mot[i])  # Ajouter un terminal compris 'E'
            i += 1
    return symbols


def generer_mot_long_infEgal_n(mot, regles, n, ens_mots, memo):
    ''' 
    Donne en sortie un ensemble de tous les mots de 'longueur <= n' générés par la grammaire
    en utilisant la programmation dynamique.

    Arguments : 
        - mot : String, initialisé au premier appel avec l'axiome.
        - regles : Dictionnaire des règles de production.
        - n : Un entier représentant la longueur maximale.
        - ens_mots : Un set qui représente l'ensemble des mots générés, initialement vide. 
        - memo : Un dictionnaire pour la mémorisation des sous-problèmes.

    '''
    # le seul mot de longeur 0 
    if n==0 and 'E' in regles[mot]:
        ens_mots.add('E')
    # Si le mot dépasse la longueur n (stop)
    if len(extraire_symboles_dans_mot(mot)) > n:
        return
    # Si ce mot a déjà été généré pour cette longueur, on évite de le recalculer
    if (mot, len(mot)) in memo:
        return
    # Si le mot contient uniquement des terminaux ,alors on l'ajoute dans l'ensemble des mots générés.
    if all(s.islower() for s in mot) or mot == "E":
        ens_mots.add(mot)
        memo[(mot, len(mot))] = True  #marquer comme deja vu
        return

    # Mémoriser pour éviter de refaire les calcules
    mot=mot.replace('E','')
    memo[(mot, len(mot))] = True
    # Extraire les symboles du mot
    symboles = extraire_symboles_dans_mot(mot)
    # Traiter les symboles non-terminaux et appliquer les règles de production
    for s in symboles:
        if s.isupper():  # Si c'est un non-terminal
            if s in regles:  # le Remplacer par ses règles de productions
                for r in regles[s]:
                    # derivation a gauche 
                    nv_mot = mot.replace(s, r, 1)
                    # Lancer la génération pour ce nouveau mot 
                    generer_mot_long_infEgal_n(nv_mot, regles, n, ens_mots, memo)


    


def main():
    if len(sys.argv)!=3:
        print("usage : python generer.py <N=longeurMax> <nomfichier>.chomsky/greibach")
        sys.exit(1)
     
    N=int(sys.argv[1])
    fichier_fn=sys.argv[2]

    #Verification de l'extension de fichier 
    if not (fichier_fn.endswith('.chomsky') or fichier_fn.endswith('.greibach')):
        raise ValueError(f"L'extension du fichier '{fichier_fn}' n'est pas valide. Utilisez un fichier avec l'extension '.chomsky' ou '.greibach'.")
    
    # Lecture de la grammaire en FN contenue dans le fichier 
    axiome,regles=lire(fichier_fn)

    #Generation de mots de longeurs <= N
    ens_mots=set()
    generer_mot_long_infEgal_n(axiome, regles, N, ens_mots,{})

    # Triee les mots generer en ordre lexicographique
    ens_mots=sorted(ens_mots)

    for mot in ens_mots:
        print(f'{mot}')

if __name__=="__main__":
    main()