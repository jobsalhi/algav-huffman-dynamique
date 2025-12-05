"""Arbre Huffman dynamique (Ayoub)."""

from .leaf_node import LeafNode
from .internal_node import InternalNode
from .update_algorithm import update_tree

class DynamicHuffmanTree:  # (Ayoub)
    """Racine, NYT, table symboles."""
    def __init__(self):
        self.root = LeafNode(is_NYT=True)
        self.NYT = self.root
        """ Map symbol -> leaf node """
        self.symbol_nodes = {}  

    def is_leaf(self, node):
        """Teste si feuille."""
        return isinstance(node, LeafNode)

    def update(self, symbol):
        """Délègue la mise à jour dynamique au module externe.

        Cette classe reste minimale (structure uniquement);
        la logique FGK/Vitter est gérée dans `core.update_algorithm`.
        """
        return update_tree(self, symbol)
