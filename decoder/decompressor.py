"""Fonctions de décompression (approche fonctions)."""

from pathlib import Path

from core.tree import DynamicHuffmanTree
from core.update_algorithm import update_tree
from utils.bitreader import lecture


def decode_file(input_path: str | Path, output_path: str | Path) -> None:
    """Décoder un binaire .huff vers un fichier de sortie (octets)."""
    tree = DynamicHuffmanTree()
    sequence = lecture(str(input_path))

    # En-tête : taille attendue sur 64 bits
    size_bits = sequence[:64]
    expected_size = int(size_bits, 2)

    n = len(sequence)
    cursor = 64
    decoded_count = 0

    with open(output_path, 'wb') as out:
        while cursor < n and decoded_count < expected_size:
            nb_bits, symbol = read_next_symbol(tree, sequence, cursor)

            if nb_bits == 0 or symbol is None:
                break

            cursor += nb_bits
            decoded_count += 1

            out.write(bytes([symbol]))
            update_tree(tree, symbol)

    return None


def read_next_symbol(tree, sequence, start_index):
    """
    Fonction principale : Lit le prochain symbole (encodé ou littéral).
    Retourne : (nombre_de_bits_consommés, symbole_décodé)
    """
    node, bits_traversed = _traverse_tree(tree, sequence, start_index)
    
    if node is None:
        return 0, None

    # NYT : lire le prochain octet brut
    if node.is_NYT:
        literal_index = start_index + bits_traversed
        char = _read_literal_byte(sequence, literal_index)

        return bits_traversed + 8, char

    # cas standard : symbole déjà connu
    return bits_traversed, node.symbol


def _traverse_tree(tree, sequence, start_index):
    """
    Descend dans l'arbre bit par bit jusqu'à trouver une feuille.
    Retourne : (le_noeud_feuille, nombre_de_bits_utilisés)
    """
    node = tree.root
    current_idx = start_index
    max_len = len(sequence)

    # Descente bit à bit jusqu'à une feuille
    while current_idx < max_len and not tree.is_leaf(node):
        bit = sequence[current_idx]
        node = node.left if bit == "0" else node.right
        current_idx += 1

    if tree.is_leaf(node):
        return node, current_idx - start_index

    return None, 0


def _read_literal_byte(sequence, start_index):
    """
    Lit 8 bits à partir de l'index donné et les convertit en caractère.
    """
    bits_lit = sequence[start_index : start_index + 8]
    return int(bits_lit, 2)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python -m decoder.decompressor <input.huff> <output.txt>")
    else:
        decode_file(sys.argv[1], sys.argv[2])

