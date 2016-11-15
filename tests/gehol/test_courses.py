from libulb.gehol import courses
from libulb.tools import Slug


def test_get_list():
    l = courses.get_list()

    assert 6000 < len(l) < 9000
    assert isinstance(l, dict)
    assert all([isinstance(x, Slug) for x in l.keys()])
    assert l[Slug('info', 'f', '101')] == "Programmation"
