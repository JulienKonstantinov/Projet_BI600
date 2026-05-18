from lpa import *


def aggregate_solution(G, solution1, solution2) :
    """Combine 2 solutions obtenues en créant des étiquettes paires"""

    dico =  {k: (solution1[k], solution2[k]) for k in solution1}

    for i in range(0, 100) :  #tant qu'on dépasse pas le max d'itération on met à jour l'étiquette selon les voisins
        labels = update_labels_async(G,dico) 

        if check_stop_criterion(G,labels):   #si on atteint le critère d'arrete on s'arrete
            break

    return labels


def run_multiple_and_aggregate(G, n=5) :
    """Lance label_propagation n fois et agrège toutes les solutions progressivement"""

    labels = label_propagation(G)  #on cherche une première solution

    for i in range(n -1 ) :   #on boucle sur n-1 car on a deja une premiere solution 
        nouvelle_solution = label_propagation(G)   #on en fait une nouvelle
        labels = aggregate_solution(G, labels, nouvelle_solution)  #on combine les 2

    return labels

        