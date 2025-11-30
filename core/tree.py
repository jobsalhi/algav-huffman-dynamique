"""Arbre Huffman dynamique (Ayoub)."""

from .leaf_node import LeafNode
from .internal_node import InternalNode

class DynamicHuffmanTree:  # (Ayoub)
    """Racine, NYT, table symboles."""
    def __init__(self):
        self.root = LeafNode(is_NYT=True)
        self.NYT = self.root
        self.symbol_nodes = {}

    def is_leaf(self, node):
        """Teste si feuille."""
        return isinstance(node, LeafNode)
