"""Fonctions de compression (approche fonctions, sans classes).

`encode_file` lit le texte symbole par symbole, gère NYT vs symbole connu,
met à jour l'arbre dynamique et écrit les bits via `BitWriter`.
"""

from pathlib import Path
from core.tree import DynamicHuffmanTree
from utils.bitwriter import ecriture
import os

def encode_file(input_path: str | Path, output_path: str | Path) -> None:
    """Encoder un fichier texte UTF-8 vers un binaire via un fichier temp."""
    
    temp_bits_path = "temp_bits.txt"
    tree = DynamicHuffmanTree()
    
    # 1. récupération de la taille exacte du fichier original (en octets)
    file_size = os.path.getsize(input_path)
    
    with open(input_path, 'rb') as f_in, \
         open(temp_bits_path, 'w', encoding='utf-8') as f_temp:
        
        # 2. écriture de la taille en binaire au tout début (sur 64 bits pour être large)
        # Cela crée une chaine de 64 '0' et '1' au début du fichier
        f_temp.write(format(file_size, '064b'))

        while True:
            byte_data = f_in.read(1)
            
            if not byte_data:
                break 
            
            symbol = byte_data[0] 
            
            bit_sequence = ""
            if tree.contains(symbol):  
                # Cas 1 : Symbole connu -> Chemin dans l'arbre
                bit_sequence = tree.get_code(symbol)
            else: 
                # Cas 2 : Nouveau symbole -> NYT + 8 bits 
                nyt_code = tree.get_nyt_code()
                char_bits = format(symbol, '08b') 
                bit_sequence = nyt_code + char_bits

            f_temp.write(bit_sequence)
            tree.update(symbol)

    ecriture(temp_bits_path, str(output_path))
    if os.path.exists(temp_bits_path):
        os.remove(temp_bits_path) # supprime le fichier temporaire utilisé avec la fonction ecriture


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage : python -m encoder.compressor <entree.txt> <sortie.huff>")
        raise SystemExit(1)

    input_arg = Path(sys.argv[1])
    output_arg = Path(sys.argv[2])

    encode_file(input_arg, output_arg)
    print(f"Compression terminée : {input_arg} -> {output_arg}")

