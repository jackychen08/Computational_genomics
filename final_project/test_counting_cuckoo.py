import pytest
from counting_cuckoo import Counting_Cuckoo


@pytest.fixture
def cuckoo():
    return Counting_Cuckoo(500, 3)


def test_insert(cuckoo):
    assert cuckoo.insert("test")
    assert cuckoo.search("test")


def test_not_there(cuckoo):
    assert not cuckoo.search("false")
