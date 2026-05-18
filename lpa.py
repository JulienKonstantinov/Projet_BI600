from collections import Counter, defaultdict
import random
import networkx as nx

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

        
def label_propagation(G, max_iter= 100) :
    """Fonction principale qui prend en entrée notre graphe G et retourne le dico {noeud : communauté}"""

    labels = initialize_labels(G)  #chaque noeud recoit comme étiquette son propre ID

    for i in range(0, max_iter) :  #tant qu'on dépasse pas le max d'itération on met à jour l'étiquette selon les voisins
        labels = update_labels_async(G,labels) 

        if check_stop_criterion(G,labels):   #si on atteint le critère d'arrete on s'arrete
            break

    return labels


def split_disconnected_communities(G, labels) : 
    """Apres la convergence la fonction detecte les grp de noeuds
      ayant la meme etiquette mais deconnectés du reste du groupe, 
      on sépare via BFS et donne de nouvelles etiquette"""
    
    groupes = {}
    for noeud, etiquette in labels.items() :  #on construit un dico {etquette : noeud} pour savoir quels noeuds ont la meme etiquette
        if etiquette not in groupes :
            groupes[etiquette] = []
        groupes[etiquette].append(noeud)

    for etiquette, j in groupes.items() :  #pour chaque groupe on extrait le sous-graphe qui contient uniquement ces nœuds et les arêtes entre eux
        sous_graphe = G.subgraph(j)
        
        if not nx.is_connected(sous_graphe) :  #on vérifie si ce sous-graphe est connexe, si c'est pas le cas il faut séparer
            composantes = list(nx.connected_components(sous_graphe))  #on récupère toutes les composantes connexes de ce sous-graphe déconnecté

            for composante in composantes[1:]:   #on parcourt toutes les composantes sauf la première qui garde son étiquette originale
                nouvelle_etiquette = list(composante)[0]
                for noeud in composante:
                    labels[noeud] = nouvelle_etiquette #on prend le premier nœud de la composante comme nouvelle étiquette unique, et on la réassigne à tous les nœuds de cette composante
    
    return labels


def get_communities(labels) :
    """Regroupe les noeuds par étiquette et retourne notre liste des communautés"""

    groupes = defaultdict(list)   #on crée un dico vide et chaque nouvelle clé aura automatiquement une liste vide
    
    for noeud, etiquette in labels.items() :  #on parcourt tout les noeuds et on ajoute les noeuds dans la liste correspondant a leur etiquette
        groupes[etiquette].append(noeud) 
    
    resultat = list(groupes.values())  #on récupère les listes de noeuds

    return resultat