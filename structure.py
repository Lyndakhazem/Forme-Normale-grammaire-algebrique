class Grammaire: 
    # Generer tous les terminaux possible 
    tous_terminaux=[chr(i) for i in range(97, 123)]
    # Générer tous les non-terminaux possibles (25 lettres majuscules sauf E * 10 chiffres)
    lettres_maj = [chr(i) for i in range(65, 91) if chr(i) != "E"]  # Lettres A à Z sauf Epsilon 
    tous_les_non_terminaux = {f"{lettre}{c}" for lettre in lettres_maj for c in [str(i) for i in range(10)] }
    
    def __init__(self,axiome,regles):
        ''' Constructeur de base 
            Arguments : 
            axiome: Le symbole de départ de la grammaire.
            regles : Dictionnaire {key:Non_term, value:List(ses regles de prod) qui represente les regles de production  
        '''
        self.axiome=axiome
        self.regles =regles
        self.terminaux,self.non_terminaux=self.extraire_symboles()

    
    def extraire_symboles(self):
        ''' Extrait depuis les regles de production l'ensemble des symboles 
            terminaux et non terminaux
        '''
        ter,var=set(),set()
        for mg,production in self.regles.items():
            var.add(mg)
            for prod in production :
                symboles=self.extraire_symboles_de_production(prod)
                for s in symboles :
                    if s.islower() and s not in ter:
                        ter.add(s)
        return ter,var 
                
    
    def extraire_symboles_de_production(self, prod):
        '''
        Découpe une production en symboles (terminaux et non-terminaux).
        Exemple : "aA1B2" sera découpé en ["a","A1", "B2"]
        prod: La production à découper (chaîne de caractères).
        return Liste des symboles separer dans l'ordre .
        '''
        symbols = []
        i = 0
        while i < len(prod):
            if prod[i].isupper() and i + 1 < len(prod) and prod[i+1].isdigit():  # Non-terminal
                symbols.append(prod[i:i+2])  
                i += 2  # On saute ces deux caractères
            else:
                symbols.append(prod[i])  # Ajouter un terminal compris E
                i += 1
        return symbols
    def ajout_regles(self,membre_g,regles):
        ''' 
        Ajoute les regles de productions contenant dans la liste regles a la variable membre_g.
        '''
        if membre_g not in self.regles:
            self.regles[membre_g]=[]
            
        for r in regles :
            if r not in self.regles[membre_g]:
                self.regles[membre_g].append(r)


    def identifier_annulables(self):
        '''
        Identifie les variables annulables (celles qui peuvent dériver en epsilon) dans la grammaire.
        Retourne un ensemble de variables annulables.
        '''
        annulables = set()

        # les variables qui produisent directement epsilon
        for mg, productions in self.regles.items():
            if "E" in productions and mg != self.axiome:  # sauf l'axiome
                annulables.add(mg)

        # Propagation des variables annulables
        for mg, productions in self.regles.items():
            for prod in productions:
                symboles = self.extraire_symboles_de_production(prod)
                # Si tous les symboles sont annulables alors X est annulable
                if all(s in annulables for s in symboles):
                    if mg not in annulables:
                        annulables.add(mg)
                    
        return annulables
    
    def variable_dispo(self):
        ''' Retourne la prochaine variable (non terminale) disponible '''
        
        return sorted(self.tous_les_non_terminaux - self.non_terminaux)[0]
    

    def __str__(self):
        ''' Retourne une représentation lisible de la grammaire sous forme de chaîne de caractères '''
        grammaire_str = f"Σ: {','.join(sorted(self.terminaux))}\n"        
        grammaire_str += f"V: {','.join(sorted(self.non_terminaux))}\n"
        grammaire_str += f"Axiome: {self.axiome}\n"
        
        for mg, productions in self.regles.items():

            grammaire_str += f"{mg} -> "
            grammaire_str += " | ".join(productions)  
            grammaire_str += "\n"
        
        return grammaire_str


