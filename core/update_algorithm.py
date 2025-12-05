"""Algorithme de mise à jour (FGK/Vitter) pour Huffman dynamique.
Squelette fonctionnel : uniquement signatures et TODO, pas d'implémentation.
"""

from .leaf_node import LeafNode
from .internal_node import InternalNode
from .node_base import NodeBase

# Entrée principale

def update_tree(tree, symbol):
    """Mettre à jour l'arbre dynamique après lecture de `symbol`.
    TODO:
    - Déterminer si `symbol` est nouveau ou déjà présent
    - Appeler `insert_new_symbol(tree, symbol)` ou `update_existing_symbol(tree, symbol)`
    - Déclencher le traitement (incréments, fin de bloc, swaps) jusqu'à la racine
    """
    pass

# Cas d'insertion / mise à jour

def insert_new_symbol(tree, symbol):
    """Insérer un nouveau symbole via le nœud NYT.
    TODO:
    - Remplacer le NYT par un nœud interne + deux enfants
    - Créer la feuille pour `symbol`
    - Mettre à jour `tree.symbol_nodes` et `tree.NYT`
    - Relier correctement parents/enfants
    """
    pass


def update_existing_symbol(tree, symbol):
    """Mettre à jour lorsque le symbole existe déjà.
    TODO:
    - Retrouver la feuille via `tree.symbol_nodes[symbol]`
    - Démarrer le traitement (incrément, finBloc, swap) sur le chemin vers la racine
    """
    pass

# Primitives de traitement

def increment_weight(node: NodeBase):
    """Incrémenter le poids du nœud.
    TODO:
    - Augmenter `node.weight` de 1
    """
    pass


def find_block_leader(tree, node: NodeBase):
    """Trouver le chef de bloc pour le poids de `node`.
    TODO:
    - Identifier le nœud de même poids avec l'indice GDBH le plus élevé
    """
    pass


def swap_nodes(tree, a: NodeBase, b: NodeBase):
    """Échanger deux nœuds selon GDBH.
    TODO:
    - Respecter la contrainte "pas d'échange avec un ancêtre"
    - Mettre à jour parents/enfants
    """
    pass


def renumber_tree(tree):
    """Renuméroter l'arbre (GDBH).
    TODO:
    - Recalculer les identifiants GDBH pour tous les nœuds
    """
    pass


def get_path_to_root(node: NodeBase):
    """Obtenir le chemin `node -> ... -> root`.
    TODO:
    - Remonter via `parent` jusqu'à la racine et retourner la liste
    """
    pass


def is_incrementable(node: NodeBase):
    """Tester la condition d'incrémentabilité locale.
    TODO:
    - Vérifier `node.parent` et comparer `node.weight < parent.weight`
    """
    pass
