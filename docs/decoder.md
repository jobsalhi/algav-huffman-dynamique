# Décodeur Huffman Dynamique

Ce document décrit le fonctionnement du décodeur `decode_file(input_path, output_path)`.

## 1) Objectif

Reconstruire exactement le fichier original (au niveau **octets**) à partir d’un fichier compressé `.huff`.

La propriété de correction principale est le **round-trip** :

`decode(encode(x)) = x` (égalité stricte des bytes).

## 2) En-tête 64 bits : taille attendue

Le fichier `.huff` commence par **64 bits** représentant la taille du fichier original en **octets**.

- le décodeur lit ces 64 bits,
- calcule `expected_size`,
- puis continue à décoder jusqu’à produire exactement `expected_size` octets.

Cela permet d’ignorer le padding éventuel du dernier octet du fichier compressé.

## 3) Symbole manipulé : l’octet (byte-level)

Comme pour l’encodeur, le décodeur manipule un symbole comme un entier dans `{0..255}`.

Même si l’entrée est un texte UTF-8, l’implémentation reconstruit les octets originaux ; un caractère UTF‑8 multi-octets (ex. emoji) correspond donc à plusieurs symboles.

## 4) Décodage d’un symbole

Le décodage se fait par parcours de l’arbre :

- on part de la racine,
- on lit les bits un à un :
	- `0` : aller à gauche,
	- `1` : aller à droite,
- on s’arrête quand on atteint une feuille.

Deux cas :

### 4.1) Feuille normale (symbole connu)

Si la feuille atteinte n’est pas NYT :

- le symbole décodé est celui stocké dans la feuille,
- on l’écrit (en binaire) dans le fichier de sortie,
- puis on met à jour l’arbre (`update_tree`).

### 4.2) Feuille NYT (nouveau symbole)

Si la feuille atteinte est NYT :

- le décodeur lit immédiatement les **8 bits suivants**,
- interprète ces 8 bits comme un octet brut,
- écrit cet octet,
- puis met à jour l’arbre (`update_tree`) : insertion via NYT + remontée FGK/Vitter.

## 5) Synchronisation avec l’encodeur

L’encodeur et le décodeur doivent :

- démarrer avec le même arbre initial (un unique NYT),
- interpréter NYT de la même manière,
- appliquer exactement la même mise à jour FGK/Vitter après chaque symbole.

Sans cette synchronisation, les arbres divergent et la suite de bits devient impossible à interpréter.
