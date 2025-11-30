# (Maelys) Implémentera la logique de décodage bit-à-bit.

class Decoder:
    """Décodeur Huffman dynamique.
    Méthode principale: decode_next_symbol(bitstream)
    - parcourt l'arbre selon les bits
    - si NYT rencontré -> lit les octets UTF-8 suivants
    - retourne (symbole, reste_bitstream)
    """
    # (Maelys) à implémenter
    def __init__(self, tree):
        self.tree = tree

    def decode_next_symbol(self, bitstream):
        """Décodage du prochain symbole à partir d'un flux de bits.
        (Maelys) implémentera la logique complète.
        """
        pass
