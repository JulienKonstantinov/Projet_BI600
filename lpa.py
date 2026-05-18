from collections import Counter
import random

def initialize_labels(G):
    """Chaque noeud du graphe recoit comme étiquette son propre ID (en gros on génère un dictionnaire de la forme {noeud : étiquette})"""
    labels = {}
    for node in G.nodes():
        labels[node] = node
    return labels


def get_neighbor_labels(G, node, labels):
    """La fonction prend le graphe G, un noeud et le dico d'étiquettes actuel (on retourne la liste des étiquettes de tout les voisins de node)"""
    return [labels[voisin] for voisin in G.neighbors(node)]


def most_frequent_label(neighbor_labels) : 
    """Choisi l'étiquette la plus prèesente chez les voisins d'un sommet x et retourne un (aléatoirement si égalité)"""
    if neighbor_labels == [] :
        return None
    else :
        frequences = Counter(neighbor_labels)
        maximum = max(frequences.values())

        resultat = [x for x, freq in frequences.items() if freq == maximum]
        etiquette = random.choice(resultat)

        return etiquette
    

def update_labels_async(G, labels) :
    """Parcourt les noeuds aléatoirement et met a chaque jour l'étiquette de chaque noeud avec most_frequent_label (de manière asynchrone)"""

    noeuds = list(G.nodes())    #on stocke tout nos noeuds dans une liste 
    random.shuffle(noeuds)   #on echange les noeuds de notre liste aléatoirement

    for i in noeuds :    #boucle pour prendre la nouvelle etiquette
        voisins = get_neighbor_labels(G, i, labels)   
        nouvelle_etiquette = most_frequent_label(voisins)

        if nouvelle_etiquette is not None :    #s'il y a une etiquette (au moins 1 voisin) on donne cette etiquette a notre noeud
            labels[i] = nouvelle_etiquette
    
    return labels


def check_stop_criterion(G, labels) : 
    """Test le cirtère d'arret, s'arrete si diCm ≥ diCj"""
    
    for noeud in G.nodes() :   #on parcourt tout les noeuds du graphe
        etiquette_actuelle = labels[noeud]  #On récupère l'étiquette que porte ce nœud en ce moment dans le dico.
        voisins_labels = get_neighbor_labels(G,noeud,labels)  #on recupure la liste des etiquettes de ses voisins
 
        if not voisins_labels :   #si le nœud n'a aucun voisin, on passe au suivant, rien à vérifier
            continue
        
        if most_frequent_label(voisins_labels) != etiquette_actuelle :  #on recupère l'étiquette majoritaire chez les voisins, si est différente de l'étiquette actuelle du nœud on retourne False immédiatement sans même regarder les autres nœuds
            return False
        
    return True    #Si on est arrivé jusqu'ici sans jamais retourner False, c'est que tous les nœuds satisfont le critère, donc on retourne True   

        
