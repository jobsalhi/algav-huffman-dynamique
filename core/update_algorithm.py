"""Algorithme de mise à jour (FGK/Vitter) pour Huffman dynamique.
"""

from .leaf_node import LeafNode
from .internal_node import InternalNode
from .node_base import NodeBase

# Entrée principale

def update_tree(tree, symbol):
    """Mettre à jour l'arbre dynamique après lecture de `symbol`."""
    
    # 1. Gestion du symbole (Nouveau vs Existant)
    if tree.contains(symbol):
        # Cas simple : on récupère la feuille existante
        q_node = tree.symbol_nodes[symbol]
    else:
        # Cas complexe : création d'une nouvelle feuille via NYT
        q_node = insert_new_symbol(tree, symbol)

    # 2. Algorithme de remontée et d'ajustement
    while q_node is not None:
        leader = find_block_leader(tree, q_node)
        if leader is not q_node and not is_ancestor(leader, q_node):
            swap_nodes(tree, leader, q_node)
        q_node.weight += 1
        q_node = q_node.parent

    # 3. Une fois l'arbre stable, on met à jour les IDs GDBH
    renumber_tree(tree)


# Cas d'insertion / mise à jour

def insert_new_symbol(tree, symbol): #correspond a modification(H,s) 
    """Insérer un nouveau symbole via le nœud NYT."""
    old_nyt = tree.NYT
    new_nyt = LeafNode(is_NYT=True)
    new_leaf = LeafNode(symbol=symbol)
    int_node = InternalNode(left=new_nyt, right=new_leaf)
    new_nyt.parent = int_node
    new_leaf.parent = int_node

    if old_nyt is tree.root: ## si l'arbre est vide 
        tree.root = int_node
        int_node.parent = None
    else:
        # Remplacement de l'ancien NYT par le sous-arbre
        parent = old_nyt.parent #on prend le parent de NYT
        int_node.parent = parent
        if parent.left is old_nyt: 
            parent.left = int_node #si l'ancien # est à gauche  
        else: 
            parent.right = int_node #si l'ancien # est à droite

    # Mise à jour des références de l'arbre
    tree.NYT = new_nyt
    tree.symbol_nodes[symbol] = new_leaf
    
    return new_leaf


# Primitives de traitement


def find_block_leader(tree, node):
    """Retourne le chef de bloc : 
    parmi tous les nœuds de même poids, celui ayant l'id GDBH le plus élevé."""
    if node is tree.root:
        return node
        
    target_weight = node.weight
    leader = node
    max_id = node.id if node.id is not None else -1

    from collections import deque
    queue = deque([tree.root])

    while queue:
        n = queue.popleft()
        
        # on traite les ids None comme -1 pour éviter les erreurs au début
        n_id = n.id if n.id is not None else -1
        if n.weight == target_weight and n_id > max_id:
            leader = n
            max_id = n_id

        # exploration classique
        if not tree.is_leaf(n):
            if n.left: queue.append(n.left)
            if n.right: queue.append(n.right)

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




def swap_nodes(tree, a, b):
    """Échange la position de deux nœuds dans l'arbre."""
    if a is b: 
        return

    par_a, par_b = a.parent, b.parent

    if tree.root is a: tree.root = b
    elif tree.root is b: tree.root = a

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
        # on attache b à l'ancien parent de a
        if par_a:
            if par_a.left is a: par_a.left = b
            else: par_a.right = b
        
        # on attache a à l'ancien parent de b
        if par_b:
            if par_b.left is b: par_b.left = a
            else: par_b.right = a
            
        # mise à jour des parents des nœuds eux-mêmes
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
    
    # 1. BFS pour collecter les noeuds selon leur profondeur
    depth_map = defaultdict(list)
    queue = deque([(tree.root, 0)])
    max_depth = 0
    
    while queue:
        node, d = queue.popleft()
        depth_map[d].append(node)
        max_depth = max(max_depth, d)
        
        if not tree.is_leaf(node):
            if node.left: queue.append((node.left, d + 1))
            if node.right: queue.append((node.right, d + 1))
            
    # 2. Assignation des IDs (De bas en haut, gauche à droite)
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

        
