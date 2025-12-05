# Lecture et Écriture de Bits (Bit I/O)

Ce fichier explique le rôle des fonctions `bitwriter` et `bitreader`
utilisées pour la compression et la décompression Huffman dynamique.

---

## 1. Pourquoi avons-nous besoin d’un BitWriter ?

L’encodeur produit un flux de bits variable, par exemple :

10111001011...


Un fichier binaire ne peut stocker que des **octets (8 bits)**.
Le BitWriter sert à :

1. accumuler les bits générés par l’encodeur
2. regrouper les bits par blocs de 8
3. convertir chaque bloc en un entier (0–255)
4. écrire ces octets dans un fichier `.huff`
5. compléter le dernier octet avec des `0` si nécessaire

---

## 2. Pourquoi avons-nous besoin d’un BitReader ?

Le décodeur lit le fichier `.huff`, qui est une suite d’octets.
Le BitReader sert à :

1. lire chaque octet
2. reconvertir cet octet en 8 bits
3. reconstruire la chaîne de bits d’origine
4. permettre au décodeur de parcourir les codes Huffman

---

## 3. Fonctions fournies

### `write_bits_to_file(bits, filepath)`
Écrit une chaîne de bits dans un fichier binaire.

### `append_bits(buffer, bits)`
Ajoute des bits au buffer accumulé.

### `read_bits_from_file(filepath)`
Lit un fichier binaire et retourne la séquence de bits correspondante.

---

## 4. Pourquoi des fonctions et pas des classes ?

- plus simple
- plus lisible pour le binôme
- le projet ne nécessite aucun état persistant
- les fonctions couvrent exactement les besoins de l’encodeur/décodeur

---

## Résumé

BitWriter et BitReader sont indispensables pour convertir entre :

- **flux de bits** (Huffman)
- **octets** (fichiers binaires)

Ils assurent le lien entre la compression logique et le stockage physique.
