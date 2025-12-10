"""Lecture de bits depuis un fichier binaire (version fonctions)."""

def lecture(fichier_bin: str) -> str:
    """
    Lit un fichier binaire et retourne une chaîne de caractères
    composée uniquement de '0' et de '1'.
    """
    bits_list = []
    with open(fichier_bin, 'rb') as f:
        # On lit tout le fichier binaire d'un coup (c'est rapide pour 120Ko)
        content = f.read()
        
    # On convertit chaque octet en bits
    for byte in content:
        # format(byte, '08b') est plus rapide et propre que bin()[2:].zfill(8)
        bits_list.append(f"{byte:08b}")
        
    # On rejoint tout à la fin (une seule allocation mémoire)
    return "".join(bits_list)

def read_utf8_bytes(sequence):
    b_data = bytes(sequence)
    return b_data.decode('utf-8')

#lecture("fichier.bin")