"""Fonctions de compression (approche fonctions, sans classes).

`encode_file` lit le texte symbole par symbole, gère NYT vs symbole connu,
met à jour l'arbre dynamique et écrit les bits via `BitWriter`.
"""

from pathlib import Path
from typing import Iterable
from core.dynamic_huffman_tree import DynamicHuffmanTree
from utils.bitwriter import ecriture

# TODO: ajouter des fonctions utilitaires (ex: get_code_for_symbol, write_utf8)

def encode_file(input_path: str | Path, output_path: str | Path) -> None:
    """Encoder un fichier texte UTF-8 vers un binaire type .huff.

    Étapes (à implémenter):
    - ouvrir le fichier texte (UTF-8), itérer les symboles
    - symbole connu: écrire le code courant
    - nouveau symbole: écrire le code NYT puis l'UTF-8 brut
    - mettre à jour l'arbre dynamique après chaque symbole
    - flush et close du BitWriter
    """
    # Squelette: pas de logique réelle pour l'instant
    tree = DynamicHuffmanTree()
    writer = ecriture(output_path)
    # ouvrir ressources, itérer, etc.
    pass
