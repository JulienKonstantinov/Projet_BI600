import networkx as nx
import matplotlib.pyplot as plt
from chargement import charger_fichier, chemin
from lpa import *
from agregation import *

G = charger_fichier(chemin)

print("Avant filtrage (toutes les composantes) :")
print("Nombre de noeuds :", G.number_of_nodes())
print("Nombre d'arêtes :", G.number_of_edges(), "\n")

composante_large = max(nx.connected_components(G), key=len)
G = G.subgraph(composante_large).copy()

print("Après filtrage (composante principale) :")
print("Nombre de noeuds :", G.number_of_nodes())
print("Nombre d'arêtes :", G.number_of_edges(), "\n")

G_final = nx.k_core(G, k=2)
print("Après réduction :")
print("Nombre de noeuds :", G_final.number_of_nodes(), "\n")

pos = nx.spring_layout(G_final, k=0.15, iterations=50)
node_sizes = [G_final.degree(n) * 10 for n in G_final.nodes()]

plt.figure(figsize=(12, 12))

nx.draw_networkx_nodes(G_final, pos, node_size=node_sizes,
                       node_color="skyblue", alpha=0.8)
nx.draw_networkx_edges(G_final, pos, edge_color="gray", alpha=0.3)
nx.draw_networkx_labels(G_final, pos, font_size=3.8, font_color="black")

plt.title("Réseau d'interactions protéiques de S.cerevisiae", fontsize=15)
plt.axis("off")
plt.show()


G_test = nx.Graph()
G_test.add_edges_from([("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")])

labels = initialize_labels(G_test)
print("-Test initialisation labels-")
print(labels)
print("Nb étiquettes == Nb noeuds :", len(labels) == G_test.number_of_nodes())
print("Toutes distinctes :", len(set(labels.values())) == len(labels))

# Test get_neighbor_labels
print("\n-Test plus proches voisins-")
print("Voisins de A :", get_neighbor_labels(G_test, "A", labels))
print("Voisins de D :", get_neighbor_labels(G_test, "D", labels))

#Test most_frequent_labes
print("-Test most_frequent_label-")
print(most_frequent_label(["A", "B", "A", "C", "A"]))  #attendu : A
print(most_frequent_label(["A", "B", "A", "B"]))        #attendu : A ou B (aléatoire)
print(most_frequent_label([]))                           #attendu : None


print("-Test update_labels_async-")
G_test = nx.Graph()
G_test.add_edges_from([("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")])

labels = initialize_labels(G_test)
print("Avant :", labels)
labels = update_labels_async(G_test, labels)
print("Après 1 itération :", labels)
labels = update_labels_async(G_test, labels)
print("Après 2 itérations :", labels)

print("-Test check_stop_criterion-")
G_test = nx.Graph()
G_test.add_edges_from([("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")])
#Cas convergé (on sait que après 2 itérations tout est C)
labels_ok = {"A": "C", "B": "C", "C": "C", "D": "C"}
print("Cas convergé :", check_stop_criterion(G_test, labels_ok))  # attendu : True

# Cas non convergé
labels_nok = {"A": "A", "B": "B", "C": "C", "D": "D"}
print("Cas non convergé :", check_stop_criterion(G_test, labels_nok))  # attendu : False


print("-Test label_propagation sur Zachary (5 runs)-")
G_zachary = nx.karate_club_graph()
for i in range(5):
    labels_zachary = label_propagation(G_zachary)
    print(f"Run {i+1} : {len(set(labels_zachary.values()))} communautés")


#Notre vrai test sur le fichier PPi
print("-Test label_propagation sur PPI (5 runs)-")
for i in range(5):
    labels_ppi = label_propagation(G_final)
    print(f"Run {i+1} : {len(set(labels_ppi.values()))} communautés")


print("-Test split_disconnected_communities-")
G_test = nx.Graph()
G_test.add_edges_from([("A", "B"), ("C", "D")])  # 2 composantes déconnectées

# On force la même étiquette sur les deux composantes
labels_test = {"A": "X", "B": "X", "C": "X", "D": "X"}
print("Avant :", labels_test)

labels_test = split_disconnected_communities(G_test, labels_test)
print("Après :", labels_test)
# attendu : A et B gardent X, C et D reçoivent une nouvelle étiquette


print("-Test get_communities-")
labels_test = {"A": "X", "B": "X", "C": "Y", "D": "Y"}
print(get_communities(labels_test))
# attendu : [['A', 'B'], ['C', 'D']]



print("-Test aggregate_solution-")
G_zachary = nx.karate_club_graph()
sol1 = label_propagation(G_zachary)
sol2 = label_propagation(G_zachary)
print("Sol 1 :", len(set(sol1.values())), "communautés")
print("Sol 2 :", len(set(sol2.values())), "communautés")

agregat = aggregate_solution(G_zachary, sol1, sol2)
print("Agrégat :", len(set(agregat.values())), "communautés")


print("-Test run_multiple_and_aggregate-")
G_zachary = nx.karate_club_graph()
agregat = run_multiple_and_aggregate(G_zachary, n=5)
print("Nombre de communautés Karaté après agrégat de 5 runs :", len(set(agregat.values())))

# Sur le vrai PPI
agregat_ppi = run_multiple_and_aggregate(G_final, n=5)
print("Nombre de communautés PPI après agrégat de 5 runs :", len(set(agregat_ppi.values())))