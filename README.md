# Projet ALGAV — Huffman Dynamique
Master 1 STL — Sorbonne Université (2025/2026)

Implémentation d’un **compresseur** et d’un **décompresseur** basés sur l’algorithme de **Huffman dynamique** pour traiter des fichiers textuels UTF-8 et produire des fichiers binaires `.huff`.

Le projet inclut :
- la structure d’arbre de Huffman adaptatif (AHA),
- l’algorithme de mise à jour (incrémentation, finBloc, échanges),
- la lecture/écriture bit-à-bit,
- les scripts `compresser` et `decompresser`,
- les tests et expérimentations,
- le rapport final.

---

## ✔️ Checklist d’avancement

### 🔧 Implémentation
- [ ] Structure de l’arbre (nœuds, parent/children)
- [ ] Numérotation GDBH
- [ ] Incrémentation + finBloc
- [ ] Échanges de nœuds
- [ ] Gestion du symbole spécial (#)
- [ ] encode_symbol()
- [ ] decode_next_symbol()

### 📂 I/O & Scripts
- [ ] Lecture UTF-8
- [ ] Écriture binaire (padding)
- [ ] Lecture binaire bit-à-bit
- [ ] Script `compresser`
- [ ] Script `decompresser`
- [ ] compression.txt
- [ ] decompression.txt

### 🧪 Tests & Analyse
- [ ] Tests simples (round-trip)
- [ ] Expériences (Gutenberg)
- [ ] Fichiers aléatoires
- [ ] Fichiers non-naturels (.json, .py, …)

### 📄 Rapport & Présentation
- [ ] Rapport (~10 pages)
- [ ] Analyse expérimentale
- [ ] Section “usage d’IA générative”
- [ ] Slides (2–3 transparents)
