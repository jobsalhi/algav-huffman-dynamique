# (Ayoub) Implémentera la logique des nœuds internes.

from .node_base import NodeBase

class InternalNode(NodeBase):
    """Nœud interne avec deux enfants (gauche / droite)."""
    # (Ayoub) à implémenter
    def __init__(self, left=None, right=None):
        super().__init__(weight=0)
        self.left = left
        self.right = right
