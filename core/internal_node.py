"""Nœud interne pour l'arbre de Huffman dynamique."""

from .node_base import NodeBase

class InternalNode(NodeBase):
    """Contient les enfants gauche et droit; ne porte pas de symbole."""
    def __init__(self, left=None, right=None):
        super().__init__(weight=0)
        self.left = left
        self.right = right
