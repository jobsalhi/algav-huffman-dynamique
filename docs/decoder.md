# Module Décodeur (Basé sur des fonctions)

Ce module fournit `decode_file(input_path, output_path)` et des fonctions auxiliaires.

- Lit les bits via `utils.bitreader.BitReader`
- Parcourt l’arbre de Huffman dynamique pour décoder les symboles
- Si le code NYT est rencontré, lit les octets UTF-8 du nouveau symbole
- Met à jour le même arbre dynamique que l’encodeur après chaque symbole

TODO :
- Implémenter les fonctions d’aide au parcours des bits
- Gérer le NYT (lecture des prochains octets en UTF-8)
- Écrire le texte décodé dans le fichier de sortie
