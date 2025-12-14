"""Arbre Huffman dynamique."""

from .leaf_node import LeafNode
from .internal_node import InternalNode
from .update_algorithm import update_tree

class DynamicHuffmanTree:
    """Racine, NYT, table symboles."""

    def __init__(self):
        self.root = LeafNode(is_NYT=True)
        self.NYT = self.root
        # Map symbol -> leaf node
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

    def contains(self, symbol):
        """Retourne True si le symbole a déjà une feuille."""
        return symbol in self.symbol_nodes

    def get_code(self, symbol):
        """Récupère la chaîne de bits (ex: '010') pour un symbole connu."""
        if symbol not in self.symbol_nodes:
            raise ValueError(f"Symbole '{symbol}' non trouvé dans l'arbre")

        node = self.symbol_nodes[symbol]
        return self._get_node_path(node)

    def get_nyt_code(self):
        """Récupère la chaîne de bits menant au noeud NYT."""
        return self._get_node_path(self.NYT)

    def _get_node_path(self, node):
        """Remonte de 'node' jusqu'à la racine pour construire le code binaire."""
        path = ""
        current = node

        # On remonte tant qu'on a un parent
        while current.parent is not None:
            parent = current.parent

            # Si on est le fils gauche, c'est '0', sinon '1'
            if parent.left is current:
                path += "0"
            else:
                path += "1"

            current = parent

        # Comme on est remonté (Feuille -> Racine), le chemin est à l'envers.
        # Il faut l'inverser pour avoir (Racine -> Feuille)
        return path[::-1]