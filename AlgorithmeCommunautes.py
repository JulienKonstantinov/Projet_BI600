import networkx as nx
import matplotlib.pyplot as plt

chemin = "/Users/julienkonstantinov/Documents/ProjetL3/Scere20071021.txt"
G = nx.Graph()

def charger_fichier(chemin):

    with open(chemin, "r") as f:
        next(f)  # ignore première ligne

        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue

            colonnes = ligne.split("\t")
            if len(colonnes) < 2:
                continue

            parties1 = colonnes[0].split("|")
            parties2 = colonnes[1].split("|")

            for p1 in parties1:
                if "uniprotkb:" in p1:
                    protA = p1.split("uniprotkb:")[1]
                    break

            for p2 in parties2:
                if "uniprotkb:" in p2:
                    protB = p2.split("uniprotkb:")[1]
                    break

            if protA and protB and protA != protB:
                G.add_edge(protA, protB)
    
    return G

G = charger_fichier(chemin)


print("Avant filtrage (toutes les composantes) :")
print("Nombre de noeuds :", G.number_of_nodes())
print("Nombre d'arêtes :", G.number_of_edges(),"\n")
            
#Composante principale
composante_large = max(nx.connected_components(G), key=len)
G = G.subgraph(composante_large).copy() #Sous-graphe avec seulement la composant la plus large

print("Après filtrage (composante principale) :")
print("Nombre de noeuds :", G.number_of_nodes())
print("Nombre d'arêtes :", G.number_of_edges(),"\n")

G_final = nx.k_core(G, k=2) #garde seulement les noeuds avec degré >= 2
print("Après réduction :")
print("Nombre de noeuds :", G_final.number_of_nodes(),"\n")

#Placement des noeuds
pos = nx.spring_layout(G_final, k=0.15, iterations=50) #organiser le graphe naturellement en “amas” lisibles

#Taille des noeuds selon degré
node_sizes = [G_final.degree(n) * 10 for n in G_final.nodes()]

#Dessin
plt.figure(figsize=(12, 12))

nx.draw_networkx_nodes(
    G_final,
    pos,
    node_size=node_sizes,
    node_color="skyblue",
    alpha=0.8
)

nx.draw_networkx_edges(
    G_final,
    pos,
    edge_color="gray",
    alpha=0.3
)

nx.draw_networkx_labels(
    G_final,
    pos,
    font_size=3.8,
    font_color="black"
)

plt.title("Réseau d'interactions protéiques de S.cerevisae", fontsize=15)
plt.axis("off")

plt.show()