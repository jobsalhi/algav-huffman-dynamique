# Encodeur Huffman Dynamique

Ce document décrit la structure et le fonctionnement général de l’encodeur utilisé pour la compression dynamique selon l’algorithme de Huffman adaptatif.  
L’objectif est d’avoir une architecture claire avant d’implémenter la logique du compresseur.

---

## 1. Rôle général de l’encodeur

L’encodeur lit un fichier texte encodé en UTF-8, transforme chaque symbole en un flux de bits selon l’algorithme de Huffman dynamique, puis écrit ce flux dans un fichier binaire `.huff`.

Il doit :

- lire le texte **symbole par symbole** ;
- produire un code binaire dépendant de l’état courant de l’arbre ;
- mettre à jour l’arbre après chaque symbole ;
- écrire les bits dans un fichier binaire en respectant le format imposé.

L’encodeur et le décodeur doivent **évoluer exactement de la même façon**, sinon la décompression devient impossible.

---

## 2. Fonctionnement global de la compression

La compression suit toujours cette séquence :

1. Lire le prochain symbole UTF-8 du fichier texte.  
2. Déterminer s’il a déjà été rencontré.  
3.  
   - **Si nouveau** → émettre `code(NYT)` + UTF-8(symbole).  
   - **Si déjà vu** → émettre `code(symbole)` obtenu dans l’arbre.  
4. Mise à jour de l’arbre via l’algorithme *Traitement / Modification*.  
5. Écrire les bits dans un buffer.  
6. Lorsque le buffer contient au moins 8 bits → produire un octet.

Ce cycle se répète pour toute la durée du fichier.

---

## 3. Gestion du NYT (Not Yet Transmitted)

Le NYT représente « tous les symboles qui ne sont jamais apparus ».

Quand l’encodeur lit un symbole **nouveau** :

1. Il émet le **code du NYT courant** (chemin de la racine vers le node NYT).  
2. Il émet directement le symbole en **UTF-8 binaire** (octet(s) réel(s)).  
3. L’arbre est mis à jour :
   - le NYT devient un nœud interne ;
   - le fils droit = feuille contenant le nouveau symbole ;
   - le fils gauche = nouveau NYT.

Ainsi, dès la première apparition, le symbole reçoit une feuille dans l’arbre.

---

## 4. Symboles déjà vus

Quand un symbole a déjà été transmis auparavant :

1. L’encodeur retrouve sa feuille instantanément grâce au dictionnaire :  
   `symbol_nodes[caractere]`.
2. Il reconstruit son code binaire en parcourant les parents jusqu’à la racine :
   - gauche = `0`
   - droite = `1`
3. Il ajoute ce code au flux sortant.
4. Il met à jour l’arbre avec l’algorithme dynamique.

Le code peut changer au cours du traitement, car les fréquences évoluent.

---

## 5. Construction du code d’un symbole

Deux cas :

### 5.1 Symbole déjà vu  
Le code est **la suite de bits obtenue en remontant de la feuille à la racine**, puis renversée.  
Chaque étape du chemin détermine un bit :

- gauche → `0`
- droite → `1`

Ce code dépend **entièrement de l’état courant de l’arbre**, donc il peut changer à chaque symbole traité.

### 5.2 Symbole nouveau  
Pour un symbole jamais vu :

1. Le code = **chemin vers le NYT**.  
2. Puis **UTF-8(symbole)**, c’est-à-dire les bits bruts de ce caractère.

Cela permet au décodeur de reconstruire l’arbre sans ambiguïté.

---

## 6. Mise à jour de l’arbre après chaque symbole

Une fois le symbole encodé, l’encodeur applique l’algorithme dynamique :

- le poids de la feuille du symbole est augmenté ;
- on remonte vers la racine en mettant à jour les poids ;
- si un nœud rencontre un autre nœud de même poids mais placé plus haut → **échange des sous-arbres** (swap FGK/Vitter) ;
- on continue jusqu’à la racine ;
- la position du NYT peut changer selon l’évolution des poids.

Le but est de maintenir les propriétés GDBH et l’ordre des blocs.

---

## 7. Gestion du flux de bits

### 7.1 Accumulation des bits  
Les codes générés sont ajoutés dans un **buffer de bits** (string ou liste de `'0'` et `'1'`).

### 7.2 Conversion en octets  
Dès que le buffer contient **au moins 8 bits**, on prend les huit premiers :

ex: "10011011" → 155


Puis on écrit cet octet dans le fichier binaire.

### 7.3 Complétion du dernier octet  
Si le buffer final contient moins de 8 bits, on ajoute des `0` à droite pour compléter l’octet.

---

## 8. Format de sortie du fichier `.huff`

Le fichier compressé contient :

- une séquence d’octets représentant les bits du flux encodé ;
- aucune table de symboles (contrairement au Huffman statique),  
  car l’arbre est reconstruit **dynamiquement** pendant la décompression.

Le fichier `.huff` est donc minimal : uniquement les bits résultants de la compression.

---

## 9. Structure du code côté encodeur

Contenu conceptuel attendu dans `encoder.py` :

- `encode_file(input_path, output_path)`  
  - ouvre le fichier texte  
  - lit symbole par symbole  
  - gère NYT ou symbole vu  
  - écrit les octets dans le fichier binaire  

- `_encode_symbol(symbol)`  
  - renvoie les bits correspondant au symbole  
  - appelle la mise à jour de l’arbre  

- `_get_code_for_node(node)`  
  - remonte vers la racine pour reconstruire le code  

- `_write_bits(bitstring)`  
  - ajoute les bits au buffer  
  - écrit les octets complets  

- interaction constante avec `DynamicHuffmanTree`

---


## 10. Exemple de déroulement pour une chaîne simple

Considérons la chaîne :

"aba"


État initial : arbre = seul NYT.

1. **Symbole 'a' (nouveau)**  
   - sortie = code(NYT) + UTF-8('a')  
   - insertion de 'a' dans l’arbre  

2. **Symbole 'b' (nouveau)**  
   - sortie = code(NYT) + UTF-8('b')  
   - insertion de 'b'  

3. **Symbole 'a' (déjà vu)**  
   - sortie = code('a') obtenu dans l’arbre  
   - mise à jour des poids → éventuels swaps  

Le flux final est la concaténation de ces trois étapes.

---

## 11. Points importants et limitations

- l’arbre change continuellement, donc le code d’un symbole change aussi ;  
- encodeur et décodeur doivent effectuer les **mêmes mises à jour** dans le même ordre ;  
- toute erreur dans `swap`, `finBloc` ou les poids rend la décompression impossible ;  
- la gestion du NYT est cruciale pour les nouveaux symboles ;  
- bien gérer l’accumulation des bits avant d’écrire au format binaire.

---

## 12. Lien avec le décodeur

Le décodeur doit :

- lire les bits dans le même ordre que l’encodeur les génère ;  
- reconstruire l’arbre exactement de la même manière ;  
- détecter correctement les cas NYT ;  
- appliquer les mêmes mises à jour après chaque symbole.

Sans synchronisation parfaite, les deux arbres divergent.

