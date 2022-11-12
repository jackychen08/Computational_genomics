import pytest
from cuckoo import Cuckoo

@pytest.fixture
def cuckoo():
    return Cuckoo(500, 3)

def test_insert(cuckoo):
    assert cuckoo.insert("test")
    assert cuckoo.search("test")

def test_not_there(cuckoo):
    assert not cuckoo.search("false")