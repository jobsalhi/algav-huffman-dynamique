Mise à jour complète du .md (à copier directement)

# Algorithme de Mise à Jour (FGK / Vitter)

## Renumérotation GDBH de l’arbre (`renumber_tree`)

```python
def renumber_tree(tree):
		"""Assigne les numéros GDBH aux nœuds.

		Ordre GDBH : Gauche → Droite → Bas → Haut
		(on numérote d'abord les nœuds les plus profonds,
		et pour un même niveau : de gauche à droite).
		"""
		from collections import defaultdict, deque

		# 1) BFS pour collecter les nœuds selon leur profondeur
		depth_to_nodes = defaultdict(list)
		queue = deque([(tree.root, 0)])
		max_depth = 0

		while queue:
				node, depth = queue.popleft()
				depth_to_nodes[depth].append(node)
				max_depth = max(max_depth, depth)

				if getattr(node, "left", None):
						queue.append((node.left, depth + 1))
				if getattr(node, "right", None):
						queue.append((node.right, depth + 1))

		# 2) Numérotation GDBH : profondeur max → 0, gauche → droite
		current_id = 1
		for depth in range(max_depth, -1, -1):      # bas → haut
				for node in depth_to_nodes[depth]:      # gauche → droite
						node.id = current_id
						current_id += 1
```

#### Exemple illustratif

Arbre :

```
		  R
    	/   \
	   A     B
	 /  \     \
   C     D     E
```

- Profondeur 0 : `R`  
- Profondeur 1 : `A, B`  
- Profondeur 2 : `C, D, E`

Après BFS :

- `depth_to_nodes[0] = [R]`  
- `depth_to_nodes[1] = [A, B]`  
- `depth_to_nodes[2] = [C, D, E]`  
- `max_depth = 2`

Numérotation GDBH (Bas → Haut, Gauche → Droite) :

- Profondeur 2 : `C, D, E` → `C.id=1`, `D.id=2`, `E.id=3`  
- Profondeur 1 : `A, B` → `A.id=4`, `B.id=5`  
- Profondeur 0 : `R` → `R.id=6`

On obtient :

```
		   R(6)
	   /        \
	 A(4)        B(5)
	 /  \          \
  C(1)  D(2)       E(3)
```

C’est exactement l’ordre Gauche → Droite → Bas → Haut décrit dans le cours, ce qui permet de définir `finBloc` comme « le nœud de même poids avec l’indice GDBH le plus grand ».

#### Choix des structures de données

- `deque` (file FIFO)  
	- utilisée pour le BFS : `append` pour enfiler, `popleft` en O(1) pour dépiler.
- `defaultdict(list)`  
	- pour `depth_to_nodes[depth].append(node)` sans tester si la clé existe.

On pourrait utiliser une liste simple et un `dict` classique, mais ce serait plus verbeux et un peu moins efficace pour la file.

#### Complexité

Soit `n` le nombre de nœuds (au plus `2*|alphabet| - 1`, donc ≤ 511 pour un alphabet de 256 symboles) :

- BFS (collecte par profondeur) : chaque nœud est enfilé et dépilé une fois → **O(n)**  
- Numérotation (boucle sur les profondeurs + nœuds) : chaque nœud est visité une fois → **O(n)**  

Donc au total :

\[
T(n) = O(n) + O(n) = O(n)
\]

Avec `n ≤ 511`, renuméroter à chaque mise à jour reste très peu coûteux en pratique.

## Explication de `insert_new_symbol(tree, symbol)`

Cette fonction correspond exactement au cas *« nouveau symbole »* décrit dans l’algorithme FGK (`Modification(H, s)`).

Lorsqu’un symbole apparaît pour la première fois, il n’existe pas encore de feuille associée dans l’arbre. On utilise alors le nœud NYT (`Not Yet Transmitted`) pour insérer ce nouveau symbole.

Logique étape par étape :

1. **Récupération de l’ancien NYT**  
	On commence par récupérer le nœud NYT courant (`old_NYT`). C’est ce nœud qui sera remplacé.

2. **Création des nouveaux nœuds**  
	On crée :
	- une nouvelle *feuille* contenant le symbole (`leaf`),
	- un *nouveau nœud NYT* (`nyt_leaf`),
	- un *nœud interne* (`int_node`) qui aura comme enfants :
	  - le nouveau NYT (à gauche),
	  - la feuille du symbole (à droite).

	Cela correspond à la transformation suivante :

	Avant :

	```
		 # (NYT)
	```

	Après insertion du symbole `s` :

	```
		  (•)
		 /   \
	   #      s
	```

3. **Mise à jour des pointeurs parents**  
	Les deux nouveaux enfants (`leaf` et `nyt_leaf`) pointent vers le nœud interne `int_node` comme parent.

4. **Remplacement de l’ancien NYT dans l’arbre**  
	- Si l’arbre ne contenait que le NYT (cas du tout premier symbole), le nœud interne devient la **nouvelle racine**.  
	- Sinon, on remplace `old_NYT` par `int_node` dans son parent, à gauche ou à droite selon le cas.

5. **Mise à jour du nouvel état de l’arbre**  
	- Le nouveau NYT devient `tree.NYT` (pour les futures insertions).  
	- La feuille contenant le symbole est ajoutée dans la table `tree.symbol_nodes` pour rendre les recherches futures en **O(1)**.

6. **Retour de la feuille du symbole**  
	La fonction renvoie la feuille `leaf`. Cela permet à `update_tree` de commencer ensuite le traitement FGK (incréments, `finBloc`, échanges) à partir de cette nouvelle feuille.

En résumé, `insert_new_symbol` transforme le nœud NYT en un petit sous-arbre : **nœud interne + nouvelle feuille + nouveau NYT**. C’est exactement ce qui est requis par l’algorithme de Huffman dynamique pour que le nouveau symbole soit intégré et puisse ensuite participer aux mises à jour de l’arbre.

## Fonction `find_block_leader(tree, node)`

Cette fonction implémente `finBloc(H, Q)` du cours :

« Retourner le nœud du bloc (même poids) ayant l’indice GDBH maximal. »

### Problème rencontré

Lors des premières insertions, les `id` sont `None`.
L’expression `n.id > leader.id` devient impossible.

### Solution

Traiter `id=None` comme `-1` :

```python
id_n = n.id if n.id is not None else -1
id_leader = leader.id if leader.id is not None else -1

if n.weight == target_weight and id_n > id_leader:
	leader = n
```

### Complexité

- BFS → O(n)
- Sélection du max → O(n)

Très faible en pratique.

## Fonction `swap_nodes(tree, a, b)`

Cette fonction est l’un des points délicats de FGK.
Elle doit échanger deux nœuds dans l’arbre sans modifier leurs sous-arbres.

### Règles du cours

- Ne jamais échanger un nœud avec un ancêtre
  (test fait dans `update_tree` avant d’appeler `swap_nodes`)
- Mettre à jour uniquement les pointeurs parent / enfants
- Cas particulier : deux nœuds sont frères
- Cas particulier : l’un des nœuds est la racine

### Cas 1 : `A` et `B` sont des frères

Dans ce cas, le parent est le même.
On échange simplement les pointeurs gauche/droite :

```python
if parentA is parentB:
	if A_is_left:
		parent.left = b
		parent.right = a
	else:
		parent.left = a
		parent.right = b
	a.parent = parent
	b.parent = parent
	return
```

### Cas 2 : cas général

On échange leurs parents respectifs :

```python
a.parent = parentB
b.parent = parentA
```

Puis on remplace `A` par `B` chez `parentA`, et `B` par `A` chez `parentB`.

### Cas 3 : racine

Si un des nœuds était la racine :

```python
tree.root = l_autre
```

### Résultat

Une opération de `swap` conserve l’arbre et respecte la structure FGK.

## Fonction `is_ancestor(a, b)`

Utilisée dans `update_tree` pour respecter la contrainte :

« On n’échange jamais un nœud avec un de ses ancêtres. »

```python
def is_ancestor(a, b):
	cur = b.parent
	while cur is not None:
		if cur is a:
			return True
		cur = cur.parent
	return False
```

## Implémentation complète de `update_tree`

Cette fonction implémente `Modification(H, s)` puis `Traitement(H, Q)` du cours.

### Modification(H, s)

- Si `s` n’est pas dans l’arbre → insertion via NYT
- Sinon → on récupère la feuille du symbole déjà existant
- On obtient ainsi un nœud `Q` à partir duquel commencer les mises à jour

### Traitement(H, Q)

Tant que `Q` n’est pas la racine :

- Trouver `leader = finBloc(H, Q)`
- Si `leader != Q` ET `leader` n’est pas un ancêtre → `swap_nodes`
- Incrémenter `Q.weight`
- Monter au parent (`Q = Q.parent`)

À la fin → renumérotation GDBH.

### Code final

```python
def update_tree(tree, symbol):
	"""Implémente Modification(H,s) + Traitement(H,Q) du cours.
	Met à jour l’arbre FGK après lecture d’un symbole.
	"""

	# 1) Cas nouveau symbole
	if symbol not in tree.symbol_nodes:
		Q = insert_new_symbol(tree, symbol)

	# 2) Cas symbole déjà vu
	else:
		Q = tree.symbol_nodes[symbol]

	# 3) Traitement FGK / Vitter
	while Q is not None:

		leader = find_block_leader(tree, Q)

		# Échange possible uniquement si pas ancêtre
		if leader is not Q and not is_ancestor(leader, Q):
			swap_nodes(tree, leader, Q)

		# Incrément
		Q.weight += 1

		# Remonter dans l’arbre
		Q = Q.parent

	# 4) Renumérotation finale
	renumber_tree(tree)
```
