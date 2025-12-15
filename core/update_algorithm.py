"""Algorithme de mise à jour (FGK/Vitter) pour Huffman dynamique."""

from .leaf_node import LeafNode
from .internal_node import InternalNode
from .node_base import NodeBase


def update_tree(tree, symbol):
    """Mettre à jour l'arbre dynamique après lecture de `symbol`."""

    # 1) Récupérer/insérer la feuille du symbole
    if tree.contains(symbol):
        q_node = tree.symbol_nodes[symbol]
    else:
        q_node = insert_new_symbol(tree, symbol)

    # 2) Remontée : échange éventuel + incrément
    while q_node is not None:
        leader = find_block_leader(tree, q_node)
        if leader is not q_node and not is_ancestor(leader, q_node):
            swap_nodes(tree, leader, q_node)
        q_node.weight += 1
        q_node = q_node.parent

    # 3) Renumérotation GDBH
    renumber_tree(tree)


# Cas d'insertion / mise à jour

def insert_new_symbol(tree, symbol):
    """Insérer un nouveau symbole via le nœud NYT."""
    old_nyt = tree.NYT
    new_nyt = LeafNode(is_NYT=True)
    new_leaf = LeafNode(symbol=symbol)
    int_node = InternalNode(left=new_nyt, right=new_leaf)
    new_nyt.parent = int_node
    new_leaf.parent = int_node

    if old_nyt is tree.root:
        tree.root = int_node
        int_node.parent = None
    else:
        parent = old_nyt.parent
        int_node.parent = parent
        if parent.left is old_nyt:
            parent.left = int_node
        else:
            parent.right = int_node

    # Mettre à jour les références
    tree.NYT = new_nyt
    tree.symbol_nodes[symbol] = new_leaf

    return new_leaf


# Primitives de traitement


def find_block_leader(tree, node):
    """Retourne le chef de bloc (poids égal, id GDBH maximal)."""
    if node is tree.root:
        return node

    target_weight = node.weight
    leader = node
    max_id = node.id if node.id is not None else -1

    from collections import deque
    queue = deque([tree.root])

    while queue:
        n = queue.popleft()

        # ids None traités comme -1
        n_id = n.id if n.id is not None else -1
        if n.weight == target_weight and n_id > max_id:
            leader = n
            max_id = n_id

        # exploration BFS
        if not tree.is_leaf(n):
            if n.left:
                queue.append(n.left)
            if n.right:
                queue.append(n.right)

    return leader

def swap_nodes(tree, a, b):
    """Échange la position de deux nœuds dans l'arbre."""
    if a is b:
        return

    par_a, par_b = a.parent, b.parent

    if tree.root is a:
        tree.root = b
    elif tree.root is b:
        tree.root = a

    # cas 1 : même parent (frères)
    if par_a is par_b:
        parent = par_a
        # on inverse gauche/droite
        if parent.left is a:
            parent.left = b
            parent.right = a
        else:
            parent.left = a
            parent.right = b
    
    # cas 2 : parents différents
    else:
        # attacher b à l'ancien parent de a
        if par_a:
            if par_a.left is a:
                par_a.left = b
            else:
                par_a.right = b

        # attacher a à l'ancien parent de b
        if par_b:
            if par_b.left is b:
                par_b.left = a
            else:
                par_b.right = a

        # mise à jour des parents
        a.parent = par_b
        b.parent = par_a


def renumber_tree(tree):
    """
    Assigne les numéros GDBH aux nœuds :
    ordre = Gauche → Droite → Bas → Haut
    i.e. on numérote d'abord les nœuds les plus profonds,
    et pour un même niveau : de gauche à droite.
    """
    from collections import deque, defaultdict

    # 1) Collecte par profondeur (BFS)
    depth_map = defaultdict(list)
    queue = deque([(tree.root, 0)])
    max_depth = 0

    while queue:
        node, d = queue.popleft()
        depth_map[d].append(node)
        max_depth = max(max_depth, d)

        if not tree.is_leaf(node):
            if node.left:
                queue.append((node.left, d + 1))
            if node.right:
                queue.append((node.right, d + 1))

    # 2) Assignation des IDs (bas -> haut, gauche -> droite)
    current_id = 1
    for d in range(max_depth, -1, -1):
        for node in depth_map[d]:
            node.id = current_id
            current_id += 1


def is_ancestor(ancestor, node):
    """Vérifie si 'ancestor' est un parent (à n'importe quel degré) de 'node'."""
    curr = node.parent
    while curr is not None:
        if curr is ancestor:
            return True
        curr = curr.parent
    return False


