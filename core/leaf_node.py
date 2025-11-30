"""Nœud feuille (Maelys)."""

from .node_base import NodeBase

class LeafNode(NodeBase):  # (Maelys)
    """Feuille: symbole ou NYT."""
    def __init__(self, symbol=None, is_NYT=False):
        super().__init__(weight=0)
        self.symbol = symbol
        self.is_NYT = is_NYT
        self.left = None
        self.right = None
