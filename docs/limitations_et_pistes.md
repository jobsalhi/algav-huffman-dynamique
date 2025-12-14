# Limitations et pistes d’amélioration

## 1) UTF‑8 traité au niveau octet

Choix actuel : symbole Huffman = **octet** (`0..255`).

- Avantages : alphabet borné, code simple, décompression robuste.
- Limite : les caractères multi-octets (accents, emoji) se traduisent par plusieurs symboles, donc la compression peut être moins bonne sur certains textes.

## 2) Overhead sur petits fichiers

Le format `.huff` contient :
- un en-tête 64 bits (8 octets),
- le coût NYT + littéral lors de la première apparition d’un symbole,
- du padding final.

Sur des fichiers très courts, il est normal d’obtenir `ratio > 1`.

## 3) Performances

Sources classiques de lenteur (observées via les temps expérimentaux) :
- opérations globales à chaque symbole (BFS complet pour chef de bloc, renumérotation complète),
- gestion des bits via des chaînes de caractères très longues et/ou fichiers temporaires.

Pistes simples (sans changer le format de sortie) :
- écrire les bits directement en binaire avec un buffer incrémental (éviter un fichier texte temporaire),
- limiter les parcours globaux répétés (structures de blocs, tables par poids),
- éviter de relire tout le `.huff` en une seule chaîne si le fichier est très grand.
