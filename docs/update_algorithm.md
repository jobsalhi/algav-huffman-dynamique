Mise à jour complète du .md (à copier directement)

# Algorithme de Mise à Jour (FGK / Vitter)

## 1. Renumérotation GDBH de l’arbre (`renumber_tree`)

```python
def renumber_tree(tree):
	"""Assigne les numéros GDBH aux nœuds.

	Ordre GDBH : Gauche → Droite → Bas → Haut
	(on numérote d'abord les nœuds les plus profonds,
	et pour un même niveau : de gauche à droite).
	"""
	from collections import deque, defaultdict

	# 1) BFS pour collecter les nœuds selon leur profondeur
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

	# 2) Numérotation GDBH : profondeur max → 0, gauche → droite
	current_id = 1
	for d in range(max_depth, -1, -1):      # bas → haut
		for node in depth_map[d]:           # gauche → droite
			node.id = current_id
			current_id += 1
```

### Exemple illustratif

Arbre :

```
	  R
	/   \
	A     B
	/ \     \
	C   D     E
```

- Profondeur 0 : `R`  
- Profondeur 1 : `A, B`  
- Profondeur 2 : `C, D, E`

Après BFS :

- `depth_map[0] = [R]`  
- `depth_map[1] = [A, B]`  
- `depth_map[2] = [C, D, E]`  
- `max_depth = 2`

Numérotation GDBH (Bas → Haut, Gauche → Droite) :

- Profondeur 2 : `C, D, E` → `C.id=1`, `D.id=2`, `E.id=3`  
- Profondeur 1 : `A, B` → `A.id=4`, `B.id=5`  
- Profondeur 0 : `R` → `R.id=6`

Résultat :

```
	     R(6)
	   /      \
	A(4)        B(5)
	/  \          \
	C(1)  D(2)       E(3)
```

**Complexité :** chaque nœud est visité au plus deux fois → `O(n)`.

---

## 2. Insertion d’un nouveau symbole (`insert_new_symbol`)

```python
def insert_new_symbol(tree, symbol):
	"""Insérer un nouveau symbole via le nœud NYT (Modification(H,s))."""
	old_nyt = tree.NYT
	new_nyt = LeafNode(is_NYT=True)
	new_leaf = LeafNode(symbol=symbol)
	int_node = InternalNode(left=new_nyt, right=new_leaf)
	new_nyt.parent = int_node
	new_leaf.parent = int_node

	if old_nyt is tree.root:
		# Premier symbole : le nœud interne devient la racine
		tree.root = int_node
		int_node.parent = None
	else:
		# Remplacer l'ancien NYT par le nouveau nœud interne
		parent = old_nyt.parent
		int_node.parent = parent
		if parent.left is old_nyt:
			parent.left = int_node
		else:
			parent.right = int_node

	tree.NYT = new_nyt
	tree.symbol_nodes[symbol] = new_leaf

	return new_leaf
```

Idée : on remplace l’ancien NYT par un petit sous-arbre interne + (nouveau NYT, nouvelle feuille). On met à jour :

- `tree.NYT` vers le nouveau NYT,
- `tree.symbol_nodes[symbol]` pour retrouver la feuille en `O(1)`.

Complexité : quelques créations et affectations de pointeurs → `O(1)`.

---

## 3. Chef de bloc (`find_block_leader`)

```python
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

		n_id = n.id if n.id is not None else -1
		if n.weight == target_weight and n_id > max_id:
			leader = n
			max_id = n_id

		if not tree.is_leaf(n):
			if n.left:
				queue.append(n.left)
			if n.right:
				queue.append(n.right)

	return leader
```

- Parcours en largeur (BFS) de tout l’arbre.
- On garde le nœud de même poids avec l’`id` maximal.
- Les `id=None` sont traités comme `-1` pour éviter les erreurs au début.

Complexité : chaque nœud est examiné au plus une fois → `O(n)`.

---

## 4. Échange de deux nœuds (`swap_nodes`)

```python
def swap_nodes(tree, a, b):
	"""Échange la position de deux nœuds dans l'arbre."""
	if a is b:
		return

	par_a, par_b = a.parent, b.parent

	# Si l'un des deux est la racine
	if tree.root is a:
		tree.root = b
	elif tree.root is b:
		tree.root = a

	# Cas 1 : même parent (frères)
	if par_a is par_b:
		parent = par_a
		if parent.left is a:
			parent.left = b
			parent.right = a
		else:
			parent.left = a
			parent.right = b

	# Cas 2 : parents différents
	else:
		if par_a:
			if par_a.left is a:
				par_a.left = b
			else:
				par_a.right = b

		if par_b:
			if par_b.left is b:
				par_b.left = a
			else:
				par_b.right = a

		a.parent = par_b
		b.parent = par_a
```

- Ne modifie pas les sous-arbres, uniquement les liens parent/enfant.
- Gère :
  - le cas où les deux nœuds sont frères,
  - le cas général (parents différents),
  - le cas où l’un des deux est la racine.

Complexité : nombre constant de pointeurs modifiés → `O(1)`.

---

## 5. Test d’ascendance (`is_ancestor`)

```python
def is_ancestor(ancestor, node):
	"""Vérifie si 'ancestor' est un parent (à n'importe quel degré) de 'node'."""
	curr = node.parent
	while curr is not None:
		if curr is ancestor:
			return True
		curr = curr.parent
	return False
```

- Utilisé pour garantir : « on n’échange jamais un nœud avec un de ses ancêtres ».
- On remonte la chaîne des parents jusqu’à la racine.

Complexité : au plus la hauteur de l’arbre → `O(h)`.

---

## 6. Mise à jour complète (`update_tree`)

```python
def update_tree(tree, symbol):
	"""Mettre à jour l'arbre dynamique après lecture de `symbol`."""

	# 1. Gestion du symbole (nouveau vs existant)
	if tree.contains(symbol):
		q_node = tree.symbol_nodes[symbol]
	else:
		q_node = insert_new_symbol(tree, symbol)

	# 2. Traitement FGK / Vitter
	while q_node is not None:
		leader = find_block_leader(tree, q_node)
		if leader is not q_node and not is_ancestor(leader, q_node):
			swap_nodes(tree, leader, q_node)
		q_node.weight += 1
		q_node = q_node.parent

	# 3. Renumérotation GDBH finale
	renumber_tree(tree)
```

Résumé :

1. **Modification(H, s)**  
   - Si symbole nouveau → `insert_new_symbol` via le NYT.  
   - Sinon → on récupère directement la feuille via `tree.symbol_nodes`.

2. **Traitement(H, Q)**  
   - Tant que `Q` n’est pas `None` :
     - chercher le chef de bloc (`find_block_leader`),
     - échanger si possible (`swap_nodes`),
     - incrémenter le poids,
     - remonter au parent.

3. **Renumérotation**  
   - Appel à `renumber_tree(tree)` pour mettre à jour tous les `id`.

Complexité par symbole : en gros `O(h + n)` (à cause de `find_block_leader` en `O(n)`), mais avec un alphabet borné (`n ≤ 511`), cela reste très raisonnable pour ce projet.
