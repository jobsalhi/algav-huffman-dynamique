# Résultats expérimentaux — Interprétation

Ce document interprète les résultats présents dans `compression_report.csv`.

## Métriques

- `original_size` : taille du fichier d’entrée (octets).
- `compressed_size` : taille du fichier `.huff` (octets).
- `ratio` : `compressed_size / original_size`.
  - `ratio < 1` : compression (gain).
  - `ratio ≈ 1` : gain faible.
  - `ratio > 1` : expansion (souvent sur fichiers très courts).
- `compression_ms`, `decompression_ms` : temps mesurés en millisecondes.

## Résumé des tendances observées (extraits)

### 1) Fichier très court : expansion (normal)
- `short.txt` : ratio = **4.0** (3B → 12B)

Interprétation : sur un fichier minuscule, l’overhead domine :
- en-tête de 64 bits (= 8 octets),
- première occurrence de symboles via NYT (+ 8 bits “littéral”),
- padding pour compléter le dernier octet.

### 2) Aléatoire biaisé : très bon ratio
- `random_biased_letters.txt` : ratio ≈ **0.217**

Interprétation : si la distribution des symboles est très concentrée (un symbole très fréquent), Huffman attribue des codes très courts au symbole dominant.

### 3) Aléatoire uniforme : gain limité
- `random_uniform_letters.txt` : ratio ≈ **0.661**

Interprétation : quand les symboles ont des fréquences proches, les codes ont des longueurs proches, donc le gain est nettement plus faible.

### 4) Texte naturel : ratio “plausible”
- `Blaise_Pascal.txt` : ratio ≈ **0.587**

Interprétation : les textes naturels ont beaucoup de redondance (espaces, lettres fréquentes, ponctuation), donc la compression est généralement correcte.

### 5) UTF‑8 riche (emoji) : faible gain
- `emojis.txt` : ratio ≈ **0.957**

Interprétation : l’implémentation compresse au niveau **octet** (byte-level). Un emoji en UTF‑8 est souvent codé sur plusieurs octets, ce qui augmente la variété des octets observés et réduit la redondance exploitable.

## Remarque importante sur les temps

Sur `Blaise_Pascal.txt` (~120KB), les temps mesurés sont très élevés (plusieurs dizaines de secondes).
C’est un indicateur d’une implémentation correcte mais peu optimisée, typiquement due à :
- une recherche du chef de bloc par parcours global de l’arbre,
- une renumérotation complète GDBH à chaque symbole,
- ou une gestion des bits basée sur de grosses chaînes intermédiaires.

Dans le rapport, on peut l’expliquer comme une limite d’implémentation (fonctionnelle mais coûteuse), et proposer des pistes (voir `limitations_et_pistes.md`).
