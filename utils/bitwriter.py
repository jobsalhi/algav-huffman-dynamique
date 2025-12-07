"""Écriture de bits dans un fichier binaire (version fonctions)."""

def ecriture(filepath1: str, filepath2: str):
    """
    Écrit une chaîne de bits contenue dans un fichier fichier dans un fichier binaire.
    """
    with open(filepath1, 'r') as f1:
        bits = f1.read().strip()

    if len(bits) % 8 != 0:
        bits += '0' * (8 - len(bits) % 8)

    bytes_out = bytearray()
    for i in range(0, len(bits), 8):
        byte_str = bits[i:i+8]
        byte_val = int(byte_str, 2)
        bytes_out.append(byte_val)

    with open(filepath2, 'wb') as f2:
        f2.write(bytes_out)

    print(bits)

ecriture("fichier_chaine.txt", "fichier.bin")