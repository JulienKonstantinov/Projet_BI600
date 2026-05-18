import networkx as nx
import matplotlib.pyplot as plt

def plot_network(G, title="Réseau PPI", communities=None):
    pos = nx.spring_layout(G, k=0.15, iterations=50)
    node_sizes = [G.degree(n) * 10 for n in G.nodes()]

    plt.figure(figsize=(12, 12))
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
                           node_color="skyblue", alpha=0.8)
    nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.3)
    nx.draw_networkx_labels(G, pos, font_size=3.8, font_color="black")
    plt.title(title, fontsize=15)
    plt.axis("off")
    plt.show()