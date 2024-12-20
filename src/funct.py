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
        #Récupérer les règles de la grammaire
        regles = G.regles
        # Trouver toutes les règles d'unité et les supprimer
        for mg, productions in list(G.regles.items()):
            # Parcourir les productions pour chaque non-terminal
            for prod in list(productions):
                # Extraire les symboles de la production
                symboles = G.extraire_symboles_de_production(prod)

                # Vérifier si la production est une règle d'unité
                if len(symboles) ==1 and symboles[0] in G.non_terminaux:
                    Y = symboles[0]
                    # Ajouter les règles de Y à X (mg)
                    if Y in regles:
                        for nv_prod in regles[Y]:
                            if nv_prod not in regles[mg]:
                                G.ajout_regles(mg,[nv_prod])
                                modification = True
                    # Supprimer la règle unité X -> Y  
                    regles[mg].remove(prod)        


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
        #Verif l'extension de fichier 
        if not input_f.endswith('.general'):
            raise ValueError(f"L'extension du fichier '{input_f}' n'est pas valide. Utilisez un fichier avec l'extension '.general'.")
        
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


# test fonctionnalites 
file="src/test.general"
axiome,dict_regles=lire(file)
g=Grammaire(axiome,dict_regles)
print("------avant operations ------------------")
print(g)
# operations
start(g);term(g);Del(g);unit(g)
print("------apres operations ------------------")
print(g)
