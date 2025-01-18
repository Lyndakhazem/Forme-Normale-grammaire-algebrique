from funct import *
import sys

def Chomsky(G):
    '''
       Transforme la grammaire algebrique generale en FN Chomsky
       Arguments:
       G : instance de la grammaire generale
    '''
    start(G);term(G);bin(G);Del(G);unit(G)


def Greibach(G):
    '''
       Transforme la grammaire algebrique generale en FN Chomsky
       Arguments:
       G : instance de la grammaire generale
    '''
    start(G);Del(G);unit(G)
    del_var_head(G)
    term_head(G)


def main():
    if len(sys.argv)!=2:
        print("usage : python grammaire.py <nomfichier>.general")
        sys.exit(1)

    fichier_general = sys.argv[1]
    #Verification de l'extension de fichier 
    if not fichier_general.endswith('.general'):
        raise ValueError(f"L'extension du fichier '{fichier_general}' n'est pas valide. Utilisez un fichier avec l'extension '.general'.")
    
    prefixe = fichier_general.split(".general")[0]

    #Lecture de la grammaire 
    print(f'Lecture de la grammaire depuis le fichier {fichier_general} ...')
    axiome,regles = lire(fichier_general)
    G=Grammaire(axiome,regles)
    print(f'Grammaire generale lu : \n {G}')

    #Deux copies identiques de la grammaire initiale
    Gc = G.copy()
    Gg = G.copy()

    fichier_chomsky = f'{prefixe}.chomsky'
    fichier_greibach = f'{prefixe}.greibach'

    #Conversion en FN chomsky
    Chomsky(Gc)
    Gc.ecrire(fichier_chomsky)
    print(f'Grammaire en FN Chomsky sauvegardée dans le fichier: {fichier_chomsky}')

    #Conversion en FN greibach
    Greibach(Gg)
    Gg.ecrire(fichier_greibach)
    print(f'Grammaire en FN Greibach sauvegardée dans le fichier: {fichier_greibach}')

if __name__ == "__main__":
    main()

        
