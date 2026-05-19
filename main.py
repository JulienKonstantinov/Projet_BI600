import networkx as nx
import matplotlib.pyplot as plt
from chargement import charger_fichier, chemin
from lpa import *
from agregation import *
from visualisation import *

G = charger_fichier(chemin)

print("Avant filtrage (toutes les composantes) :")
print("Nombre de noeuds :", G.number_of_nodes())
print("Nombre d'arêtes :", G.number_of_edges(), "\n")

composante_large = max(nx.connected_components(G), key=len)
G = G.subgraph(composante_large).copy()

print("Après filtrage (composante principale) :")
print("Nombre de noeuds :", G.number_of_nodes())
print("Nombre d'arêtes :", G.number_of_edges(), "\n")

G_final = nx.k_core(G, k=1)
print("Après réduction :")
print("Nombre de noeuds :", G_final.number_of_nodes(), "\n")

plot_network(G_final, title="Réseau PPI brut de S. cerevisiae")

# Schéma 2 - coloré par communauté après 1 run
labels_ppi = label_propagation(G_final)
plot_network(G_final, title="Communautés après 1 run", labels=labels_ppi)

# Schéma 3 - coloré après agrégation
agregat_ppi = run_multiple_and_aggregate(G_final, n=5)
plot_network(G_final, title="Communautés après agrégation de 5 runs", labels=agregat_ppi)

# Schéma 4 : distribution des communuatés 
communautes_ppi = get_communities(agregat_ppi)
plot_size_distribution(communautes_ppi, title="Distribution des tailles de communautés PPI")


