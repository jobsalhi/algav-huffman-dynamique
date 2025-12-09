"""Algorithme de mise à jour (FGK/Vitter) pour Huffman dynamique.
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
    # if symbol in tree.symbol_nodes:
    #      node = tree.symbol_nodes[symbol]
    # else:
    #     node = insert_new_symbol(tree, symbol)
    # pass


    # node.weight+= 1 

# Cas d'insertion / mise à jour

def insert_new_symbol(tree, symbol):   #correspond a modification(H,s) 
    """Insérer un nouveau symbole via le nœud NYT."""
    old_NYT = tree.NYT
    leaf = LeafNode(symbol=symbol)
    nyt_leaf = LeafNode(is_NYT=True)
    int_node = InternalNode(nyt_leaf,leaf)
    leaf.parent = int_node
    nyt_leaf.parent = int_node
    if old_NYT is tree.root :  ## si l'arbre est vide 
        tree.root = int_node
        int_node.parent = None

    else:
        parent = old_NYT.parent   #on prend le parent de NYT
        if parent.left is old_NYT:   #si l'ancien # est a gauche  
            parent.left = int_node
        else:
            parent.right = int_node   #si l'ancien # est a gauche 
        int_node.parent = parent

    tree.NYT = nyt_leaf
    tree.symbol_nodes[symbol] = leaf 
    return leaf





# Primitives de traitement


def find_block_leader(tree, node):
    """Retourne le chef de bloc pour `node` :
    parmi tous les nœuds de même poids, celui ayant l'id GDBH le plus élevé.
    """
    target_weight = node.weight
    leader = node  # au minimum, le nœud lui-même

    # BFS pour visiter tous les nœuds
    from collections import deque
    queue = deque([tree.root])

    while queue:
        n = queue.popleft()

        # on ne garde que les nœuds avec le même poids
        if n.weight == target_weight and n.id > leader.id:
            leader = n

        # exploration classique
        if getattr(n, "left", None):
            queue.append(n.left)
        if getattr(n, "right", None):
            queue.append(n.right)

    return leader


# -----------------------------------------------------------
# NOTE (Ayoub): Tentative optimisation idea
#
# Hypothèse : faire un parcours BFS en priorité droite→gauche,
# et retourner le premier nœud rencontré ayant le poids recherché.
# Cela reproduit souvent l’ordre GDBH inverse dans de nombreux cas,
# car l’arbre de Huffman dynamique garde une structure assez équilibrée.
#
# Exemple d’idée :
#
# queue = deque([tree.root])
# while queue:
#     n = queue.popleft()
#     if n.weight == target_weight:
#         return n
#     if n.right: queue.append(n.right)
#     if n.left:  queue.append(n.left)
#
# Statut : cette approche semble fonctionner sur de nombreux exemples,
# mais n'est pas garantie par la théorie FGK. À tester plus tard avec
# des séquences aléatoires pour comparer son comportement au finBloc exact.
# -----------------------------------------------------------




def swap_nodes(tree, a: NodeBase, b: NodeBase):
    """Échanger deux nœuds selon GDBH.
    TODO:
    - Respecter la contrainte "pas d'échange avec un ancêtre"
    - Mettre à jour parents/enfants
    """
    pass



def renumber_tree(tree):
    """
    Assigne les numéros GDBH aux nœuds :
    ordre = Gauche → Droite → Bas → Haut
    i.e. on numérote d'abord les nœuds les plus profonds,
    et pour un même niveau : de gauche à droite.
    """
    from collections import defaultdict, deque

    # 1) BFS pour collecter les noeuds selon leur profondeur
    depth_to_nodes = defaultdict(list)
    queue = deque([(tree.root, 0)]) # on commance par le root
    max_depth = 0

    while queue:
        node, depth = queue.popleft() 
        depth_to_nodes[depth].append(node)
        max_depth = max(max_depth, depth)

        if getattr(node, "left", None):  #getattr(obj, attribute_name, default_value) # either it get the attribute and gives none back
            queue.append((node.left, depth + 1)) # on utilise getattr car les feullies ont pas les attributes left et right donc ça pose des problems 
        if getattr(node, "right", None):
            queue.append((node.right, depth + 1))

    # 2) Numérotation GDBH : profondeur max → 0, gauche → droite
    current_id = 1
    for depth in range(max_depth, 0 - 1, -1):   # bas → haut
        for node in depth_to_nodes[depth]:      # gauche → droite
            node.id = current_id
            current_id += 1
