"""Lecture de bits depuis un fichier binaire (version fonctions)."""


def lecture(fichier_bin: str) -> str:
    """
    Lit un fichier binaire et retourne une chaîne de caractères
    composée uniquement de '0' et de '1'.
    """
    bits_list = []
    with open(fichier_bin, 'rb') as f:
        # Lire tout le fichier binaire
        content = f.read()

    # On convertit chaque octet en bits
    for byte in content:
        bits_list.append(f"{byte:08b}")

    # On rejoint tout à la fin (une seule allocation mémoire)
    return "".join(bits_list)
