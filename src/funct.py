from structure import Grammaire

def start(G):
    '''
    Retire l'axiome de G des membres droit des regles .
    Modifie la grammaire passée en parametre .
    Arguments : instance de la Structure Grammaire
    '''
    G.non_terminaux.add("S") # Ajout d'une nouvelle variable 
    G.regles["S"]=[G.axiome]#Ajout de la regle S->Ancien axiome
    G.axiome="S" #S nouveau axiome

def term(G):
    '''
    Supprime les termainaux de membre droit des regles de long>=2
    Modifie la grammaire passée en parametre .
    Arguments : instance de la Structure Grammaire
    '''
    fait = {}
    for mg, productions in list(G.regles.items()):
        for prod in list(productions):
            symboles=G.extraire_symboles_de_production(prod)
            if len(symboles) > 1:  # Ne traiter que les productions de longuer au moin 2
                nouvelle_prod = ""
                for symbole in symboles:
                    if symbole.islower():  # Si terminal
                        if symbole not in fait:
                            # Nouveau non-terminal
                            nv=G.variable_dispo()
                            G.non_terminaux.add(nv)
                            fait[symbole] = nv  
                            G.ajout_regles(fait[symbole],[symbole])# Associer terminal -> non-terminal
                        nouvelle_prod += fait[symbole]  # Remplacer par non-terminal
                    else:
                        nouvelle_prod += symbole  # Conserver non-terminaux
                # Mettre à jour la règle
                G.regles[mg].remove(prod)
                G.ajout_regles(mg,[nouvelle_prod])

def bin(G):
    '''
    Supprime les regles avec plus de 2 Non terminaux a droite
    Modifie la grammaire passée en parametre .
    Arguments : instance de la Structure Grammaire
    '''
    modifications = True  # vérifier si des modifications ont eu lieu
    while modifications:
        modifications=False
        for mg, productions in list(G.regles.items()):
            for prod in list(productions):
                #Découpe la production en symboles
                symboles = G.extraire_symboles_de_production(prod)
                # Si la production contient plus de 2 non-terminaux
                if len(symboles) > 2: 
                    modifications = True #grammaire modifié
                    nv=G.variable_dispo()# Créer un nouveau non-terminal
                    G.non_terminaux.add(nv)
                    # Suppression et Ajout la nouvelle production avec le premier non-terminal et le nouveau
                    G.regles[mg].remove(prod)
                    G.ajout_regles(mg,[symboles[0] + nv])
                    # Créer une nouvelle règle avec le non-terminal introduit pour les symboles suivants
                    G.ajout_regles(nv,[''.join(symboles[1:])])
                    symboles=[symboles[0], nv]

def Del(G):
    '''
    Supprime les regles X->E(epsilon) sauf si X est l'axiome
    Modifie la grammaire passée en parametre .
    Arguments : instance de la Structure Grammaire
    '''
    annulables=G.identifier_annulables()

    for mg, productions in list(G.regles.items()):
        for prod in list(productions):
            symboles = G.extraire_symboles_de_production(prod)
            # Si existe une ou plsr variables dans la production sont annulables
            if any(s in annulables for s in symboles):
                nouvelles_productions = set()

                # Générer une nouvelle production en supprimant les symboles annulables
                for i in range(2**len(symboles)):  # On génère toutes les combinaisons de symboles annulables
                    new_prod = []
                    for j in range(len(symboles)):
                        # Si le symbole n'est pas annulable 
                        # ou si il est annulable et on a décide de le garder
                        if (symboles[j] not in annulables) or (i & (1 << j)):  
                            new_prod.append(symboles[j])

                    if new_prod:
                        nouvelles_productions.add("".join(new_prod))
                    else: 
                        nouvelles_productions.add("".join("E"))

                # Maj regles productions de X=mg
                G.regles[mg].remove(prod)
                G.ajout_regles(mg,nouvelles_productions)
        

    # Supprimer les règles epsilon restantes (sauf l'axiome)
    for mg, productions in list(G.regles.items()):
        if mg != G.axiome:  # sauf axiome 
            if "E" in productions:
                G.regles[mg].remove("E")
        if productions==[]:
            del G.regles[mg]
            
def unit(G):
    '''
    supprime les regles unite X->Y , X et Y sont des non terminaux
    Modifie la grammaire passée en parametre .
    Arguments : instance de la Structure Grammaire'''

    modification = True
    while modification:
        modification = False
        # Trouver toutes les règles d'unité et les supprimer
        for mg, productions in list(G.regles.items()):
            # Parcourir les productions pour chaque non-terminal
            for prod in list(productions):
                # Extraire les symboles de la production
                symboles = G.extraire_symboles_de_production(prod)

                # Vérifier si la production est une règle d'unité
                if len(symboles) ==1 and symboles[0] in G.non_terminaux:
                    Y = symboles[0]
                    # Supprimer la règle unité X -> Y  
                    G.regles[mg].remove(prod)
                    # Ajouter les règles de Y à X (mg)
                    G.ajout_regles(mg,G.regles[Y])
                    modification = True        

def sup_recursion_gauche(G):
    '''
    supprime la recursion gauche 
    exemple : A0 -> A0a | b    =>  A0 -> bA1 | b
                                   A1 -> aA1|a
    Modifie la grammaire passée en paramètre.
    Arguments : instance de la Structure Grammaire
    '''
    for mg, productions in list(G.regles.items()):
        nv_non_term = G.variable_dispo()
        for prod in list(productions):
            symboles = G.extraire_symboles_de_production(prod)
            if symboles[0] == mg:
                if nv_non_term not in G.non_terminaux:
                    G.non_terminaux.add(nv_non_term)
                reste = "".join(symboles[1:])
                nv_regle = [reste,reste+nv_non_term]
                G.ajout_regles(nv_non_term, nv_regle)
                G.regles[mg].remove(prod)
            elif nv_non_term in G.non_terminaux:
                G.ajout_regles(mg,[prod+nv_non_term])



def del_var_head(G):
    '''
    Supprime les non-terminaux en tête des règles
    compris la suppression de la recursion gauche
    Exemple : A0 -> B0a | b
              B0 ->c | d  résultat A0 -> ca | da |b
                                   B0 -> c| d
    Modifie la grammaire passée en paramètre.
    Arguments : instance de la Structure Grammaire
    '''
    sup_recursion_gauche(G)
    modification = True
    while modification:
        modification = False
        for mg, productions in list(G.regles.items()):
            for prod in list(productions):
                symboles = G.extraire_symboles_de_production(prod)
                if symboles[0] in G.non_terminaux:
                    t = symboles[0]
                    nv_productions = []
                    reste = "".join(symboles[1:])
                    for p in G.regles[t]:
                        nv_productions.append(p+reste)
                    G.regles[mg].remove(prod)
                    G.ajout_regles(mg,nv_productions)
                    modification = True
        

        

def term_head(G):
    '''
    Supprime les symboles terminaux qui ne sont pas en tête des règles.
    Cette fonction transforme chaque terminal qui n'est pas en tête d'une règle en un nouveau non-terminal,
    et les remplace dans les règles correspondantes.
    Modifie la grammaire passée en paramètre.
    Arguments : instance de la Structure Grammaire
    '''
    # Associe chaque terminal à un nouveau non-terminal
    terminal_to_non_terminal = {}
    for mg, productions in list(G.regles.items()):       
        for prod in list(productions):            
            symboles = G.extraire_symboles_de_production(prod) 
            
            # Liste pour stocker la production modifiée
            nouvelle_prod = symboles[0]

            # Parcours des symboles dans la production
            for s in symboles[1:]:
                if s in G.terminaux and s.islower():  # Si c'est un terminal, on le remplace

                    # Vérifie si un non-terminal existe déjà pour ce terminal
                    if s not in terminal_to_non_terminal:
                        nv_non_term = G.variable_dispo()  # Nouveau non-terminal pour le terminal
                        G.non_terminaux.add(nv_non_term) # ajouter ce nv non terminaux aux non_terminaux de la grammaire
                        terminal_to_non_terminal[s] = nv_non_term  # Associe le terminal au nouveau non-terminal
                        G.ajout_regles(nv_non_term, [s])

                    # Utilise le non-terminal existant
                    nouvelle_prod +=terminal_to_non_terminal[s]
                else:
                    nouvelle_prod+=s  # Si ce n'est pas un terminal, on garde le symbole tel quel

            # Une fois qu'on a modifié les symboles, on met à jour les règles
            G.regles[mg].remove(prod)
            G.ajout_regles(mg, [nouvelle_prod])


def dic_regles(input_l):
    '''
    transforme une liste de tuple representant les regles de production
    en un dictionnaire de regles de prod. 
    exp:[("S","aS2"),("S2","b")("S2","E")] => dic({"S":["aS2"],
                                                "S2":["b","E"]} )
    '''
    d={}
    for mg,md in input_l :
        if mg in d.keys() and md not in d[mg]:d[mg].append(md)
        else: d[mg]=[md]
    return d 

def lire(input_f):
    ''' 
    permet de lire un fichier contenant une grammaire et la stocker dans votre structure
    de données. L'extension du fichier doit être ".general" pour général.
    Return : l'axiome et dict des regles de productions si pas d'erreur dans le fich source .
    '''
    try:
        l=[]
        # Lecture du fichier
        with open(input_f, 'r', encoding='utf-8') as f:
            for ligne in f:
                # Supprimer les espaces inutiles
                ligne = ligne.strip().replace(" ", "")
                # Ignorer les lignes vides
                if not ligne:
                    continue
                
                # Vérifier si la ligne est bien formée
                if ':' not in ligne:
                    raise ValueError(f"Ligne mal formée : {ligne}")
                
                # Séparer membre_gauche et membre_droit
                membre_gauche, membre_droit = ligne.split(':', 1)
                
                # Ajouter la règle à la grammaire
                # Le membre_droit peut être une liste de sous-règles
                l.append((membre_gauche,membre_droit))
        axiome=l[0][0]
        regles=dic_regles(l)
        return axiome,regles
        
    except FileNotFoundError:
        print(f"Erreur : Le fichier {input_f} est introuvable.")
        return None
    except ValueError as e:
        print(f"Erreur de format : {e}")
        return None
