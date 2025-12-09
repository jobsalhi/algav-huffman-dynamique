from core.tree import DynamicHuffmanTree
from core.update_algorithm import update_tree
from core.leaf_node import LeafNode


def print_tree(node, indent="", is_right=True):
    """Affichage clair d'un arbre binaire tourné à 90°.
    Le sous-arbre droit est affiché en haut, le gauche en bas.
    """

    if node is None:
        return

    # Afficher d'abord le fils droit
    print_tree(getattr(node, "right", None), indent + "    ", True)

    # Construire label lisible
    if isinstance(node, LeafNode):
        if getattr(node, "is_NYT", False):
            label = f"NYT"
        else:
            label = f"'{node.symbol}'"
    else:
        label = "*"

    w = getattr(node, "weight", "?")
    idx = getattr(node, "id", "?")

    connector = "┌──" if is_right else "└──"
    print(f"{indent}{connector} {label} (w={w}, id={idx})")

    # Afficher fils gauche
    print_tree(getattr(node, "left", None), indent + "    ", False)


def print_full_tree(tree, title=""):
    print("\n" + "=" * 60)
    if title:
        print(title)
        print("-" * 60)

    if tree.root is None:
        print("(arbre vide)")
        print("=" * 60)
        return

    print_tree(tree.root)
    print("=" * 60)


def main():
    tree = DynamicHuffmanTree()
    sequence = "ABACA"

    print_full_tree(tree, "État initial (seulement NYT)")

    for i, s in enumerate(sequence, start=1):
        print(f"\n>>> update_tree(tree, '{s}')  (symbole #{i})")
        update_tree(tree, s)
        print_full_tree(tree, f"Après insertion/mise à jour du symbole '{s}'")

    print("\nSéquence traitée :", sequence)
    print(
        "symbol_nodes :",
        {k: f"w={v.weight}, id={getattr(v, 'id', '?')}" for k, v in tree.symbol_nodes.items()},
    )


if __name__ == "__main__":
    main()
