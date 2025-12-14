# Encodeur Huffman Dynamique

Ce document décrit le fonctionnement de l’encodeur `encode_file(input_path, output_path)`.

## 1) Objectif

Compresser un fichier texte encodé en UTF‑8 dans un fichier binaire `.huff` via **Huffman dynamique** (FGK/Vitter).

Contrairement à Huffman statique :

- l’arbre évolue après chaque symbole,
- le code d’un symbole peut changer au cours du flux,
- aucune table de codes n’est stockée dans le fichier compressé.

## 2) Symbole manipulé : l’octet (byte-level)

L’encodeur lit le fichier en binaire (`rb`) et traite chaque **octet** comme un symbole Huffman (entier dans `{0..255}`).

Conséquence : un caractère UTF‑8 multi-octets (accent, emoji, etc.) est vu comme plusieurs symboles.

## 3) NYT (Not Yet Transmitted)

L’arbre contient une feuille spéciale **NYT** (notée `#` dans l’énoncé), représentant “tout symbole jamais vu”.

Pour chaque octet `b` lu :

- si `b` est déjà connu : on émet `code(b)`
- sinon : on émet `code(NYT)` puis `b` sur 8 bits (valeur brute)

Puis, dans les deux cas : on met à jour l’arbre avec `update_tree(tree, b)`.

## 4) En-tête 64 bits

Le fichier `.huff` commence par **64 bits** représentant la taille (en octets) du fichier original.

Cela permet au décodeur de :

- savoir combien d’octets reconstruire,
- ignorer le padding éventuel du dernier octet.

## 5) Émission des bits et écriture binaire

L’encodeur produit un flux de bits (codes Huffman + littéraux après NYT). Pour l’écrire dans un fichier binaire :

- on regroupe les bits par paquets de 8,
- on convertit chaque paquet en octet,
- si le dernier paquet est incomplet : padding à droite avec des `0`.

## 6) Synchronisation encodeur/décodeur

Le décodeur ne reçoit aucune table de symboles. La synchronisation repose uniquement sur :

- la présence de NYT pour distinguer “nouveau symbole” vs “symbole connu”,
- l’en-tête 64 bits,
- la mise à jour FGK/Vitter strictement identique des deux côtés.

