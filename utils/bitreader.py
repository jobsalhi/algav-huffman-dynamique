"""Lecture de bits depuis un fichier binaire (version fonctions)."""

def lecture(filepath: str) -> str:
    """
    Lit un fichier binaire et retourne une chaîne de bits.
    """
    with open(filepath, 'rb') as f:
        bytes_data = f.read()

    bits = ''.join(format(byte, '08b') for byte in bytes_data)
    print(bits)
    return bits

lecture("fichier.bin")