import networkx as nx
import matplotlib.pyplot as plt
from chargement import charger_fichier, chemin

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