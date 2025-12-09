from core.tree import DynamicHuffmanTree
from core.update_algorithm import update_tree
from core.leaf_node import LeafNode


def print_tree(node, prefix="", is_left=True):
    """Affiche l'arbre de manière textuelle (poids + id + symbole/NYT)."""
    if node is None:
        return

    connector = "└── " if is_left else "┌── "

    # Construire l'étiquette du nœud
    label_parts = []

    if isinstance(node, LeafNode):
        if getattr(node, "is_NYT", False):
            label_parts.append("NYT")
        else:
            label_parts.append(f"'{node.symbol}'")
    else:
        label_parts.append("*")  # nœud interne

    label_parts.append(f"w={getattr(node, 'weight', '?')}")
    label_parts.append(f"id={getattr(node, 'id', '?')}")

    label = " ".join(label_parts)
    print(prefix + connector + label)

    child_prefix = prefix + ("    " if is_left else "│   ")

    if getattr(node, "left", None) is not None:
        print_tree(node.left, child_prefix, True)
    if getattr(node, "right", None) is not None:
        print_tree(node.right, child_prefix, False)


def print_full_tree(tree, title=""):
    """Affiche la racine et appelle print_tree sur ses enfants."""
    print("\n" + "=" * 60)
    if title:
        print(title)
        print("-" * 60)

    if tree.root is None:
        print("(arbre vide)")
        print("=" * 60)
        return

    root = tree.root
    label_parts = []

    if isinstance(root, LeafNode):
        if getattr(root, "is_NYT", False):
            label_parts.append("NYT")
        else:
            label_parts.append(f"'{root.symbol}'")
    else:
        label_parts.append("*")

    label_parts.append(f"w={getattr(root, 'weight', '?')}")
    label_parts.append(f"id={getattr(root, 'id', '?')}")
    print("ROOT:", " ".join(label_parts))

    if getattr(root, "left", None) is not None:
        print_tree(root.left, "", True)
    if getattr(root, "right", None) is not None:
        print_tree(root.right, "", False)

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
