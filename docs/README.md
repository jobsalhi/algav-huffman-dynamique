# Documentation — Huffman Dynamique (ALGAV)

Ces fichiers `.md` servent de base pour le rapport (explications simples, cohérentes avec l’implémentation du dépôt).

## Vue d’ensemble

- [encoder.md](encoder.md) : fonctionnement du compresseur (Huffman dynamique, symboles = octets).
- [decoder.md](decoder.md) : fonctionnement du décompresseur (symétrie avec l’encodeur).
- [lecture_et_ecriture_de_bits.md](lecture_et_ecriture_de_bits.md) : conventions bit-à-bit + padding + en-tête 64 bits.
- [structure_de_l_arbre.md](structure_de_l'arbre.md) : structure des nœuds et de l’arbre (NYT, dictionnaire d’accès direct).
- [update_algorithm.md](update_algorithm.md) : mise à jour FGK/Vitter (insertion, chef de bloc, swaps, renumérotation GDBH).
- [execution_et_imports.md](execution_et_imports.md) : exécuter avec `python -m` + scripts `compresser`/`decompresser`.
- [resultats_experimentaux.md](resultats_experimentaux.md) : lecture et interprétation de `compression_report.csv`.
- [limitations_et_pistes.md](limitations_et_pistes.md) : limites connues + pistes d’amélioration.
- [usage_ia.md](usage_ia.md) : section demandée sur l’usage d’IA (à compléter).

## Points de cohérence (important)

- Les fichiers d’entrée sont en UTF-8, mais l’implémentation traite le flux au niveau **octet** : un symbole Huffman est un entier dans `{0..255}`.
- Le fichier `.huff` commence par **64 bits** encodant la taille attendue (en octets) du fichier original.
- L’arrêt de décompression se fait sur un compteur d’octets (`expected_size`), ce qui permet d’ignorer le padding final.
