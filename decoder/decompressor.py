"""Fonctions de décompression (approche fonctions, sans classes).

`decode_file` lit des bits, reconstruit les symboles avec l'arbre dynamique,
gère NYT vs codes connus, met à jour l'arbre, et écrit la sortie UTF-8.
"""

from pathlib import Path
from core.tree import DynamicHuffmanTree
from utils.bitreader import BitReader

# TODO: ajouter des fonctions utilitaires (ex: read_next_symbol_bits, read_utf8_bytes)

def decode_file(input_path: str | Path, output_path: str | Path) -> None:
    """Décoder un binaire type .huff vers un fichier texte UTF-8.

    Étapes (à implémenter):
    - ouvrir le binaire et itérer les bits via BitReader
    - parcourir l'arbre avec les bits pour trouver un symbole; si NYT, lire UTF-8 brut
    - mettre à jour l'arbre dynamique après chaque symbole décodé
    - écrire le texte UTF-8 décodé dans la sortie
    - fermer les ressources
    """
    tree = DynamicHuffmanTree()
    reader = BitReader(input_path)
    # ouvrir ressources, itérer, etc.
    pass
