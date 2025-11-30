# (Ayoub) Mettra en place la structure et la logique d'évolution.

from .leaf_node import LeafNode
from .internal_node import InternalNode

class DynamicHuffmanTree:
    """Structure principale de l'arbre Huffman dynamique.
    Attributs:
        - root: racine de l'arbre (initialement NYT)
        - NYT: référence vers le nœud NYT courant
        - symbol_nodes: dictionnaire symbole -> nœud feuille
    """
    # (Ayoub) structure de base, logique à implémenter ensuite
    def __init__(self):
        self.root = LeafNode(is_NYT=True)
        self.NYT = self.root
        self.symbol_nodes = {}

    def is_leaf(self, node):
        """Retourne True si le nœud est une feuille."""
        return isinstance(node, LeafNode)
