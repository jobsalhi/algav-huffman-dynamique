"""BitReader: lit des octets et expose les bits un par un.
Squelette minimal; pas de logique de lecture réelle pour l'instant.
"""

class BitReader:
    """Lire des bits depuis un fichier binaire, MSB d'abord dans les octets."""
    def __init__(self, input_path):
        self.input_path = input_path
        self._file = None
        self._buffer = b""
        self._index = 0
        self._bitpos = 0

    def open(self):
        """Ouvrir le fichier binaire en lecture."""
        pass

    def read_bit(self):
        """Retourner le prochain bit (0/1) ou None à l'EOF."""
        pass

    def read_bits(self, n: int) -> str:
        """Retourner les n prochains bits sous forme de chaîne."""
        pass

    def close(self):
        """Fermer le fichier."""
        pass
