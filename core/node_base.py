"""Nœud de base (Ayoub)."""

class NodeBase:  # (Ayoub)
    """Nœud générique: poids, parent, id. -> structure partager par les feuilles et neuds internes """
    def __init__(self, weight=0):
        self.weight = weight
        self.parent = None
        self.id = None
