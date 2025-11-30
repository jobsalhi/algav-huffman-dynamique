# (Maelys) Implémentera la logique spécifique d'un nœud feuille.

from .node_base import NodeBase

class LeafNode(NodeBase):
    """Nœud feuille représentant un symbole ou le nœud NYT.
    Attributs:
        - symbol: caractère associé (None pour NYT)
        - is_NYT: booléen indiquant s'il s'agit du nœud "Not Yet Transmitted"
        - left / right: inclus pour compatibilité structure (pas utilisés pour une feuille)
    """
    # (Maelys) à implémenter
    def __init__(self, symbol=None, is_NYT=False):
        super().__init__(weight=0)
        self.symbol = symbol
        self.is_NYT = is_NYT
        self.left = None
        self.right = None
