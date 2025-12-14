# Projet ALGAV — Huffman Dynamique
Master 1 STL — Sorbonne Université (2025/2026)

Langage : **Python 3.12.2**

Implémentation d’un **compresseur** et d’un **décompresseur** basés sur l’algorithme de **Huffman dynamique** pour traiter des fichiers textuels UTF-8 et produire des fichiers binaires `.huff`.

Le projet inclut :
- la structure d’arbre de Huffman adaptatif (AHA),
- l’algorithme de mise à jour (incrémentation, finBloc, échanges),
- la lecture/écriture bit-à-bit,
- les scripts `compresser` et `decompresser`,
- les tests et expérimentations,
- le rapport final.

---

## Checklist d’avancement

### Implémentation
- [x] Structure de l’arbre (nœuds, parent/children)
- [x] Numérotation GDBH
- [x] Incrémentation + finBloc
- [x] Échanges de nœuds
- [x] Gestion du symbole spécial (#)
- [ ] encode_symbol()
- [ ] decode_next_symbol()

### I/O & Scripts
- [x] Lecture UTF-8
- [x] Écriture binaire (padding)
- [x] Lecture binaire bit-à-bit
- [x] Script `compresser`
- [x] Script `decompresser`
- [x] compression.txt
- [x] decompression.txt

---

## Format du rendu (I/O strict)

### Commandes

- Compression : `./compresser input.txt output.huff`
- Décompression : `./decompresser input.huff output.txt`

Les scripts Bash `compresser` et `decompresser` appellent respectivement `compresser.py` et `decompresser.py`.

### Logs

À chaque exécution, une ligne est ajoutée au fichier correspondant :

- `compression.txt` (format exact, séparateur `;`) :
	`input_path;output_path;input_bytes;output_bytes;ratio;time_ms`
	où `ratio = output_bytes / input_bytes` (5 décimales).

- `decompression.txt` (format exact, séparateur `;`) :
	`input_path;output_path;input_bytes;output_bytes;ratio;time_ms`
	où `ratio = output_bytes / input_bytes` (5 décimales).


### Tests & Analyse
- [ ] Tests simples (round-trip)
- [ ] Expériences (Gutenberg)
- [ ] Fichiers aléatoires
- [ ] Fichiers non-naturels (.json, .py, …)

### Rapport & Présentation
- [ ] Rapport (~10 pages)
- [ ] Analyse expérimentale
- [ ] Section “usage d’IA générative”
- [ ] Slides (2–3 transparents)
