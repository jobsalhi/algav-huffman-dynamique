"""Nœud feuille pour l'arbre de Huffman dynamique (NYT ou symbole)."""

from .node_base import NodeBase

class LeafNode(NodeBase):
    """Représente un symbole ou le nœud NYT."""
    def __init__(self, symbol=None, is_NYT: bool = False):
        super().__init__(weight=0)
        self.symbol = symbol
        self.is_NYT = is_NYT
        self.left = None
        self.right = None
