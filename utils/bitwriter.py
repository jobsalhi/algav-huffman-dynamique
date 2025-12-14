"""Écriture de bits dans un fichier binaire (version fonctions)."""

def ecriture(fichier_chaine: str, fichier_bin: str):
    """
    Lit un fichier textuel contenant une chaîne de bits ("010101...")
    et écrit un fichier binaire en regroupant les bits par octets.
    """

    # Lire la chaîne de bits
    with open(fichier_chaine, 'r') as f1:
        bits = f1.read().strip()

    # Compléter les bits pour un multiple de 8
    if len(bits) % 8 != 0:
        bits += '0' * (8 - len(bits) % 8)

    # Conversion en octets
    bytes_out = bytearray()
    for i in range(0, len(bits), 8):
        byte_str = bits[i : i + 8]
        bytes_out.append(int(byte_str, 2))

    # Écriture binaire
    with open(fichier_bin, 'wb') as f2:
        f2.write(bytes_out)

