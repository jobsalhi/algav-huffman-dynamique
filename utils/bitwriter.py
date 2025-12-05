"""BitWriter: tamponne des bits et écrit des octets dans un fichier.
Squelette minimal; pas de logique d'écriture réelle pour l'instant.
"""

class BitWriter:
    """Écrit des bits, les regroupe en octets, et les écrit dans un fichier."""
    def __init__(self, output_path):
        self.output_path = output_path
        self._buffer = 0
        self._count = 0
        self._file = None

    def open(self):
        """Ouvrir le fichier binaire en écriture."""
        pass

    def write_bit(self, bit: int):
        """Ajouter un bit (0 ou 1) au tampon."""
        pass

    def write_bits(self, bits: str):
        """Ajouter une chaîne de bits comme '10101'."""
        pass

    def flush(self):
        """Écrire le tampon courant en dernier octet (avec padding)."""
        pass

    def close(self):
        """Flusher et fermer le fichier."""
        pass
