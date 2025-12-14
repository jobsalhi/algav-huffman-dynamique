# Lecture et écriture de bits (Bit I/O)

Ce fichier explique la conversion entre :

- un flux de bits (codes Huffman),
- et un fichier binaire (octets).

Dans ce projet, ces conversions sont gérées par :

- `utils.bitwriter.ecriture(...)` : écrit une chaîne de bits dans un fichier binaire
- `utils.bitreader.lecture(...)` : lit un fichier binaire et retourne la chaîne de bits

---

## 1) Pourquoi avons-nous besoin d’un BitWriter ?

L’encodeur produit un flux de bits variable, par exemple :

10111001011...


Un fichier binaire ne stocke que des **octets (8 bits)**. Pour écrire un flux de bits variable :

1. regrouper les bits par blocs de 8
2. convertir chaque bloc en un entier (0–255)
3. écrire ces octets dans un fichier `.huff`
4. compléter le dernier octet avec des `0` si nécessaire (padding)

---

## 2) Pourquoi avons-nous besoin d’un BitReader ?

Le décodeur lit le fichier `.huff`, qui est une suite d’octets.
Le BitReader sert à :

1. lire chaque octet
2. reconvertir cet octet en 8 bits
3. reconstruire la chaîne de bits d’origine
4. permettre au décodeur de parcourir les codes Huffman

---

## 3) Fonctions utilisées dans ce dépôt

### `utils.bitwriter.ecriture(fichier_chaine, fichier_bin)`
Lit un fichier texte contenant une chaîne de bits (`"0101..."`) et écrit le fichier binaire.
Si le nombre de bits n’est pas multiple de 8, un padding de `0` est ajouté à droite.

### `utils.bitreader.lecture(fichier_bin)`
Lit un fichier binaire octet par octet et reconstruit la chaîne de bits correspondante.

---

## 4) Lien avec l’en-tête 64 bits

Le fichier `.huff` commence par **64 bits** encodant la taille attendue (en octets) du fichier original.

- l’encodeur écrit ces 64 bits en premier,
- le décodeur lit ces 64 bits et s’arrête après avoir reconstruit exactement `expected_size` octets.

---

## Résumé

Le BitWriter/BitReader permet de relier :

- la logique Huffman (flux de bits),
- le stockage sur disque (octets).
