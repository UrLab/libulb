from libulb.tools import Slug
import pytest


@pytest.fixture
def slug1():
    return Slug('info', 'f', '101')


def test_outputs(slug1):
    assert slug1.gehol == "INFOF101"
    assert slug1.catalog == "INFO-F101"
    assert slug1.dochub == "info-f-101"


def test_2_digit():
    Slug('info', 'y', '56')
