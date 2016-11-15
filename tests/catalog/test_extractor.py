from libulb.catalog import extractor


def test_ba_info():
    tree = extractor.get_approximate_tree("ba-info")
    assert isinstance(tree, list)
    assert 'Bachelier en sciences informatiques' in tree[0]
