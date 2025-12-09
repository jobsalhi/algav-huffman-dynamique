"""Fonctions de décompression (approche fonctions, sans classes).

`decode_file` lit des bits, reconstruit les symboles avec l'arbre dynamique,
gère NYT vs codes connus, met à jour l'arbre, et écrit la sortie UTF-8.
"""

from pathlib import Path
from core.tree import DynamicHuffmanTree
from utils.bitreader import lecture

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
    reader = lecture(input_path)
    i = 0
    # ouvrir ressources, itérer, etc.
    while i<len(reader):
        i+=8
    pass

def exists_in_tree(noeud,sequence : str):
    """
    noeud : Node
    sequence : str de taille > 0
    """
    next = which_child(noeud, sequence[0])
    if len(sequence) == 1 :
        return isinstance(next, LeafNode)
    elif isinstance(next, LeafNode) or next is None:
        return False
    else :
        return exists_in_tree(next, sequence[1:])

def which_child(noeud, bin):
    if bin == 0:
        return noeud.left
    else : 
        return noeud.right