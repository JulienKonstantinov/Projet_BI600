import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def plot_network(G, title="Réseau PPI", labels=None):
    pos = nx.spring_layout(G, k=0.15, iterations=50)
    node_sizes = [G.degree(n) * 10 for n in G.nodes()]

    if labels is None:
        node_colors = ["steelblue" for n in G.nodes()]
    else:
        communautes = list(set(labels.values()))
        couleurs = cm.tab20(np.linspace(0, 1, len(communautes)))
        couleur_map = {c: couleurs[i] for i, c in enumerate(communautes)}
        node_colors = [couleur_map[labels[n]] for n in G.nodes()]

    plt.figure(figsize=(12, 12))
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
                           node_color=node_colors, alpha=0.8)
    nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.3)
    nx.draw_networkx_labels(G, pos, font_size=3.8, font_color="black")
    plt.title(title, fontsize=15)
    plt.axis("off")
    plt.show()


def plot_size_distribution(communities, title="Distribution des tailles de communautés"):
    
    tailles = sorted([len(c) for c in communities], reverse=True)
    
    x = sorted(set(tailles))
    y = [sum(1 for t in tailles if t >= s) / len(tailles) for s in x]
    
    # Droite de régression en log-log
    coeffs = np.polyfit(np.log(x), np.log(y), 1)
    alpha = coeffs[0]
    x_fit = np.array(x)
    y_fit = np.exp(coeffs[1]) * x_fit ** alpha
    
    plt.figure(figsize=(8, 6))
    plt.loglog(x, y, 'o', color="steelblue", label="Données")
    plt.loglog(x_fit, y_fit, '--', color="red", label=f"Régression α={alpha:.2f}")
    plt.xlabel("Taille de communauté (s)")
    plt.ylabel("P(S ≥ s)")
    plt.title(title)
    plt.legend()
    plt.show()
