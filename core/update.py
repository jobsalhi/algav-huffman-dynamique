# (Ayoub) Implémentera tout l'algorithme de mise à jour (incrémentation, finBloc, échanges).

class TreeUpdater:
    """Gestion des mises à jour de l'arbre Huffman dynamique.
    Méthodes à implémenter:
        - modification(symbol)
        - traitement(node)
        - finBloc(node)
        - swap_nodes(a, b)
    """
    # (Ayoub) à implémenter intégralement
    def __init__(self, tree):
        self.tree = tree

    def modification(self, symbol):
        """Met à jour l'arbre après apparition d'un symbole."""
        pass

    def traitement(self, node):
        """Traitement standard (incrément / éventuels échanges)."""
        pass

    def finBloc(self, node):
        """Gestion de la fin de bloc pour réordonnancement si nécessaire."""
        pass

    def swap_nodes(self, a, b):
        """Échange deux nœuds selon les règles de l'algorithme."""
        pass
