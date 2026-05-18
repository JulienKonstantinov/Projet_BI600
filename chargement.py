import networkx as nx
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
chemin = os.path.join(BASE_DIR, "Scere20071021.txt")

def charger_fichier(chemin):
    G = nx.Graph()
    with open(chemin, "r") as f:
        next(f)

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