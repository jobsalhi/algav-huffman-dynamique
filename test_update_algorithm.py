from core.tree import DynamicHuffmanTree
from core.update_algorithm import (
    insert_new_symbol,
    swap_nodes,
    renumber_tree,
    find_block_leader,
)


def test_insert_two_symbols():
    tree = DynamicHuffmanTree()

    # Insérer 'A'
    leafA = insert_new_symbol(tree, "A")
    assert tree.root is not None
    assert tree.root.right is leafA
    assert tree.symbol_nodes["A"] is leafA
    assert tree.NYT is tree.root.left

    # Insérer 'B'
    leafB = insert_new_symbol(tree, "B")
    assert tree.symbol_nodes["B"] is leafB
    assert tree.NYT is not None
    assert getattr(tree.NYT, "is_NYT", False) is True


def test_renumber_tree_simple():
    tree = DynamicHuffmanTree()
    leafA = insert_new_symbol(tree, "A")
    leafB = insert_new_symbol(tree, "B")

    tree.root.weight = 2
    tree.root.left.weight = 0
    leafA.weight = 1
    leafB.weight = 1

    renumber_tree(tree)

    nodes = [tree.root, tree.root.left, leafA, leafB]
    for n in nodes:
        assert getattr(n, "id", None) is not None


def test_swap_nodes_brothers():
    tree = DynamicHuffmanTree()
    leafA = insert_new_symbol(tree, "A")
    leafB = insert_new_symbol(tree, "B")

    parent = leafA.parent
    left_before = parent.left
    right_before = parent.right

    swap_nodes(tree, parent.left, parent.right)

    assert parent.left is right_before
    assert parent.right is left_before
    assert parent.left.parent is parent
    assert parent.right.parent is parent


def test_swap_nodes_general_case():
    tree = DynamicHuffmanTree()
    leafA = insert_new_symbol(tree, "A")
    leafB = insert_new_symbol(tree, "B")
    leafC = insert_new_symbol(tree, "C")

    a = leafA
    c = leafC
    parentA = a.parent
    parentC = c.parent

    swap_nodes(tree, a, c)

    assert a.parent is parentC
    assert c.parent is parentA
    assert (parentA.left is c) or (parentA.right is c)
    assert (parentC.left is a) or (parentC.right is a)


def test_find_block_leader():
    tree = DynamicHuffmanTree()
    leafA = insert_new_symbol(tree, "A")
    leafB = insert_new_symbol(tree, "B")
    leafC = insert_new_symbol(tree, "C")

    leafA.weight = 1
    leafB.weight = 1
    leafC.weight = 1

    renumber_tree(tree)

    leader = find_block_leader(tree, leafA)

    assert leader.weight == leafA.weight
    for node in [leafA, leafB, leafC]:
        if node.weight == leafA.weight:
            assert leader.id >= node.id


if __name__ == "__main__":
    test_insert_two_symbols()
    test_renumber_tree_simple()
    test_swap_nodes_brothers()
    test_swap_nodes_general_case()
    test_find_block_leader()
    print("All update_algorithm tests passed.")
