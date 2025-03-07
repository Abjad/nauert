import nauert


def test_UnweightedSearchTree___init___01():
    search_tree = nauert.UnweightedSearchTree()
    assert search_tree.definition == search_tree.default_definition


def test_UnweightedSearchTree___init___02():
    definition = {2: None, 3: {2: None}}
    search_tree = nauert.UnweightedSearchTree(definition)
    assert search_tree.definition == definition
