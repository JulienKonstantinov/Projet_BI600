from collections import deque # pour FIFO

def creer_graphe() : 
    '''Fonction qui demande à l'utilisateur les sommets et les arêtes et retourne le graphe'''
    #On implémente un graphe non orienté
    graphe = {}

    #On entre les sommets 
    sommets = input("Entrez les sommets (sous forme d'alphabet) du graphe").split()

    for s in sommets : 
        graphe[s] = []

    #On entre les arêtes
    print("Entrez les arêtes, mettre 0 quand c'est fini")
    while True : 
        arete = input("Arête")
        if arete == "0" : 
            break
        u, v = arete.split("-")

        #On ajoute les aretes dans les deux sens car on est dans le cas d'un graphe non orienté
        graphe[u].append(v)
        graphe[v].append(u)
    
    return graphe


def afficher_graphe(graphe) :
    '''Fonction qui affiche le graphe'''
    for s in graphe :
        print(s, ":", graphe[s])  #on affiche le graphe sous la forme :  sommets : [liste voisins]


def copier_graphe(graphe) : 
    '''Copie le graphe (nécessaire pour les algos divisif)'''
    copie = {}
    for s, v in graphe.items() :  #On parcourt chaque sommet et tout ses voisins
        copie[s] = list(v)  #On copie la liste des voisins

    return copie


def voisins(graphe,noeud) : 
    '''Retourne tout les voisins d'un noeud donné'''

    return graphe[noeud]


def degre(graphe) : 
    '''Renvoie le degré de chaque noeud'''
    degre = {}
    for n,v in graphe.items() :    #On parcourt le dico avec les noeuds et voisins
        degre[n] = len(v)

    return degre

def nombre_aretes(graphe):
    '''Retourne le nombre d'arêtes dans le graphe'''
    nombre = 0
    sommets_visites = set()
    for sommet, voisins in graphe.items():
        for voisin in voisins:
            if (voisin, sommet) not in sommets_visites and sommet != voisin: # pour éviter de compter deux fois la même arete
                sommets_visites.add((sommet, voisin))
                nombre += 1
    return nombre


def bfs(graphe, source):
    '''Effectue un parcours en largeur (BFS) à partir d' un noeud source'''
    #Initialisation
    distances = {sommet: float('inf') for sommet in graphe} # def distances (inf)
    predecessseurs = {sommet: [] for sommet in graphe}  #liste des prédecessuers (vide)

    distances[source] = 0 #def source distance à 0

    file = deque([source])  #on utilise FIFO pour les noeuds, avec source en fond de pile

    while file:# tant que la pile n'est pas vide
        sommet_courant = file.popleft() #extrait le premier nœud de la file avec popleft()

        for voisin in graphe[sommet_courant]:
            if distances[voisin] == float('inf'): #si jamais vu le voisin, c'est un chemin plus court
                distances[voisin] = distances[sommet_courant] + 1
                predecessseurs[voisin] = [sommet_courant]
                file.append(voisin)
            elif distances[voisin] == distances[sommet_courant] + 1:
                predecessseurs[voisin].append(sommet_courant)

    return distances, predecessseurs


def plus_court_chemin(graphe, source):
    '''Calcule les plus courts chemins depuis un nœud source vers tous les autres noeuds'''
    #Initialisation  
    distances, predecessseurs = bfs(graphe, source) #on prend BFS pour avoir les plus courts chemins
    nombre_chemins = {sommet: 0 for sommet in graphe} #le nombre de chemins à 0 pour tous
    nombre_chemins[source] = 1  #le nombre de chemins à 1 pour source (chemin vide)

    file = deque([source])  #on utilise FIFO pour les noeuds, avec source en fond de pile

    while file:
        sommet_courant = file.popleft()
        for voisin in graphe[sommet_courant]:
            #si voisin distance égale à distances[sommet_courant]+1 alors nœud courant permet un plus court chemin vers ce voisin.
            if distances[voisin] == distances[sommet_courant] + 1:  
                nombre_chemins[voisin] += nombre_chemins[sommet_courant]
                #Si nb chemin vers voisin égal au nb chemins du nœud courant alors nouveau chemin vers ce voisin depuis nœud courant
                if nombre_chemins[voisin] == nombre_chemins[sommet_courant]:
                    file.append(voisin)

    return distances, nombre_chemins, predecessseurs


def compo_connexe(graphe):
    deja_visite=set()
    compo=[]
    
    def profondeur(noeud, compo_2):
        '''On fait le parcours en profondeur pour voir tous les noeuds'''
        deja_visite.add(noeud)
        compo_2.append(noeud)
        for voisin in graphe[noeud]:
            if voisin not in deja_visite:
                profondeur(voisin, compo_2)

    for sommet in graphe:
        if sommet not in deja_visite:
            compo_2 = []
            profondeur(sommet, compo_2)
            compo.append(compo_2)

    return compo


def voisins_communs(graphe, u, v) : 
    '''Renvoi les voisins communs entre deux sommets'''
    if u not in graphe or v not in graphe:   #on vérifie que les 2 sommets sont dans le graphe
        return set()
    
    communs = set()
    
    for voisin in graphe[u]:     #on doit parcourir chaque voisin de u et verifier si c'est aussi un voisin de v
        if voisin in graphe[v]:
            communs.add(voisin)  #si c'est le cas on l'ajoute
    
    return communs