from libulb.catalog import treeextractor


def test_ba_info():
    tree = treeextractor.get_approximate_tree("ba-info")
    assert isinstance(tree, list)
    assert 'Bachelier en sciences informatiques' in tree[0]
