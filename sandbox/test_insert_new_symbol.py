from core.tree import DynamicHuffmanTree
from core.update_algorithm import insert_new_symbol

def main():
    tree = DynamicHuffmanTree()
    print("Before insert:")
    print("root:", tree.root)
    print("NYT:", tree.NYT)

    leafA = insert_new_symbol(tree, 'A')

    print("\nAfter insert 'A':")
    print("root type:", type(tree.root).__name__)
    print("root.left is NYT:", tree.root.left is tree.NYT)
    print("root.right.symbol:", tree.root.right.symbol)
    print("symbol_nodes['A'] is leafA:", tree.symbol_nodes['A'] is leafA)
    print("leafA.parent is root:", leafA.parent is tree.root)

if __name__ == "__main__":
    main()
