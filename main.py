import fonctions as f

if __name__ == "__main__":
    g = f.creer_graphe()      
    
    print("\nGraphe original :")
    f.afficher_graphe(g)    

    g2 = f.copier_graphe(g)

    print("\nCopie du graphe :")
    f.afficher_graphe(g2)

    g2['A'].append('D')
    g2['D'].append('A')

    print("\nAprès modification de la copie :")
    print("Original :")
    f.afficher_graphe(g)

    print("Copie :")
    f.afficher_graphe(g2)

    print("\nVoisins de A dans le graphe original :")
    print(f.voisins(g, "A"))

    print("\nVoisins de A dans la copie :")
    print(f.voisins(g2, "A")) 

    print("\nDegré des noeuds dans le graphe original : ")
    print(f.degre(g))

    print("\nDegré des noeuds dans la copie : ")
    print(f.degre(g2))

    print("\nNombre d'arêtes dans le graphe original")
    print(f.nombre_aretes(g))

    print("\nNombre d'arêtes dans la copie")
    print(f.nombre_aretes(g2))


#Pour l'instant pour le test j'utilise A,B,C,D avec A-B,  A-C et C-D.  Quand t'excecutes le code ca va te demander de mettre les sommets tu les mets chacun espacé d'un espace du style : A B C D 
#Ensuite tu mets les arêtes une à une en mettant entrée à chaque fois, genre : A-B entrée, A-C entrée... et quand c'est fini tu mets 0 entrée
#Pour l'instant le programme affiche le graphe de base et une copie, ensuite il rajoute un lien A-D dans la copie pour qu'on confirme que ca n'a pas changé le graphe initial
#Ensuite ca affiche tout les voisins de A dans les 2 graphes 
#A la fin ca affiche le degré de chaque noeud dans le graphe de base et la copie
