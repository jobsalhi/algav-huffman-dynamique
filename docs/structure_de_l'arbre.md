# Structure de l’arbre de Huffman dynamique

Ce document décrit la structure interne de l'arbre utilisé dans notre projet de compression selon l’algorithme de Huffman dynamique. L'objectif est de maintenir un arbre binaire qui évolue au fur et à mesure de la lecture des symboles lors de la compression et de la décompression.

---

## 1. Types de nœuds

L'arbre est composé de deux types de nœuds, tous dérivés d'une classe de base commune.

### 1.1 NodeBase (classe parente)

Attributs partagés :

- `weight` : fréquence du nœud  
- `parent` : pointeur vers le parent  
- `id` : numéro GDBH utilisé pour les échanges  

Tous les nœuds, feuilles ou internes, héritent de cette structure commune.

---

### 1.2 LeafNode (nœud feuille)

Représente :

- un symbole (dans notre implémentation : un **octet**, donc un entier dans `{0..255}`),
- ou le nœud spécial NYT (`#`, “Not Yet Transmitted”).

Attributs spécifiques :

- `symbol`  
- `is_NYT` (vrai uniquement pour le nœud #)  
- `left = None`, `right = None` (une feuille n'a pas d'enfants)

**Remarque - Pourquoi `left` et `right` existent dans une feuille ?**  
Même si une feuille ne possède pas d'enfants, il est pratique de lui attribuer les attributs `left` et `right` initialisés à `None`.  
Cela permet :

- d’unifier la structure de tous les nœuds (internes et feuilles)  
- d’éviter des erreurs lors du parcours de l’arbre (le code peut appeler `node.left` sans vérifier le type du nœud)  
- de simplifier la logique du décodeur, qui s’arrête naturellement en rencontrant une feuille (`left` et `right` sont `None`)

C'est une pratique standard dans les structures d'arbres binaires.

---

### 1.3 InternalNode (nœud interne)

Représente la structure interne de l’arbre. Ne contient aucun symbole.

Attributs :

- `left` : enfant gauche  
- `right` : enfant droit  

Le poids d’un nœud interne est la somme des poids de ses enfants.

---

## 2. État initial de l’arbre

Au début de la compression ou décompression, l’arbre contient uniquement une feuille NYT (`#`).


Ce nœud représente tous les symboles encore jamais vus. Dès qu’un nouveau symbole apparaît, il sera inséré à partir de ce nœud.

---

## 3. Classe DynamicHuffmanTree

Cette classe gère l’ensemble de l’arbre et maintient les éléments essentiels pour l’algorithme.

### 3.1 `root`  
Pointeur vers la racine de l’arbre.

### 3.2 `NYT`  
Pointeur vers le nœud NYT courant (ce pointeur évolue lorsque l'arbre se modifie).

### 3.3 `symbol_nodes`
Dictionnaire permettant de retrouver rapidement la feuille correspondant à un symbole.

Dans ce projet :

- clé : l’octet (entier),
- valeur : la feuille (`LeafNode`).

Cela permet une recherche en temps constant lors de la compression (et évite de parcourir l’arbre).

### 3.4 `is_leaf(node)`  
Fonction utilitaire :

```python
return isinstance(node, LeafNode)
```

Permet de déterminer si un nœud est une feuille (utile pour la décompression).

---

## 4. Exemple après lecture du premier symbole

Après avoir lu un premier symbole (octet), l’arbre devient :

```
     (*)
   /     \
NYT        'a'
```

(*) : nœud interne

NYT : nouveau nœud NYT

'a' : feuille contenant le symbole 'a'

---

## 5. Rôle de l’arbre dans l’algorithme

L'arbre fournit les opérations essentielles :

- retrouver le code d’un symbole en suivant le chemin racine → feuille,
- insérer un nouveau symbole via le nœud NYT,
- mettre à jour les poids des nœuds,
- appliquer les échanges (swaps) selon les règles FGK/Vitter,
- décoder des bits en parcourant l’arbre.

La classe `DynamicHuffmanTree` sert donc de structure centrale pour le compresseur, le décompresseur et l’algorithme de mise à jour.

---

## Résumé

- L’arbre commence avec un unique nœud NYT.
- Chaque symbole rencontré devient un nœud feuille.
- Les nœuds internes structurent l’arbre et ne contiennent jamais de symbole.
- La classe `DynamicHuffmanTree` gère la racine, le NYT actuel et l’accès rapide aux feuilles.

Cette structure est indispensable pour maintenir et ajuster dynamiquement les codes de Huffman.


