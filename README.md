# Projet ALGAV — Huffman Dynamique
Master 1 STL — Sorbonne Université (2025/2026)

## Environnement (langage / versions)

- Langage : **Python**
- Version : **Python 3.12.2**
- Compilateur / interpréteur utilisé : **CPython 3.12.2**

Implémentation d’un **compresseur** et d’un **décompresseur** basés sur l’algorithme de **Huffman dynamique** pour traiter des fichiers textuels UTF-8 et produire des fichiers binaires `.huff`.

Le projet inclut :
- la structure d’arbre de Huffman adaptatif (AHA),
- l’algorithme de mise à jour (incrémentation, finBloc, échanges),
- la lecture/écriture bit-à-bit,
- les scripts `compresser` et `decompresser`,
- les tests et expérimentations,
- le rapport final.

---

## Utilisation (format du rendu)

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

---

## Documentation

- Documentation technique : [docs/README.md](docs/README.md)
- Rapport LaTeX : [report/rapport_algav_huffman_dynamique.tex](report/rapport_algav_huffman_dynamique.tex)
