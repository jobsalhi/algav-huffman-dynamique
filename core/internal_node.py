"""Nœud interne (Ayoub)."""

from .node_base import NodeBase

class InternalNode(NodeBase):  # (Ayoub)
    """Interne: left, right."""
    def __init__(self, left=None, right=None):
        super().__init__(weight=0)
        self.left = left
        self.right = right
