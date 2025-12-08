# Algorithme de Mise à Jour 

### Renumérotation GDBH de l’arbre (`renumber_tree`)

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
