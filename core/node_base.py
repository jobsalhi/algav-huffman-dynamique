"""Base node for Dynamic Huffman tree.
TODO: keep minimal; actual logic later.
"""

class NodeBase:
    """Common fields: weight, parent, id (GDBH)."""
    def __init__(self, weight: int = 0):
        self.weight = weight
        self.parent = None
        self.id = None  # GDBH number
