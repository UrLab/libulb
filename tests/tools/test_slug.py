from libulb.tools import Slug
import pytest


@pytest.fixture
def slug1():
    return Slug('info', 'f', '101')


def test_gehol_output(slug1):
    assert slug1.gehol == "INFOF101"
