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



