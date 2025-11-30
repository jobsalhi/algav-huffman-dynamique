# (Ayoub) Implémentera la logique de la classe NodeBase.

class NodeBase:
    """Classe de base pour les nœuds de l'arbre Huffman dynamique.
    Attributs:
        - weight: poids (fréquence cumulée)
        - parent: référence vers le parent
        - id: identifiant GDBH (numérotation de l'arbre)
    """
    # (Ayoub) à implémenter
    def __init__(self, weight=0):
        self.weight = weight
        self.parent = None
        self.id = None
