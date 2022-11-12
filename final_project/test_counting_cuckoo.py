import pytest
from counting_cuckoo import Counting_Cuckoo


@pytest.fixture
def cuckoo():
    return Counting_Cuckoo(500, 3)


def test_insert(cuckoo):
    assert cuckoo.insert("test")
    assert cuckoo.search("test")


def test_insert_full(cuckoo):
    for i in range(4364):
        assert cuckoo.insert(str(i))
    for i in range(4364):
        assert cuckoo.search(str(i))


def test_insert_overfilled(cuckoo):
    try:
        for i in range(8000):
            cuckoo.insert(str(i))
    except Exception as e:
        assert str(e) == "Reached max size"


def test_not_there(cuckoo):
    assert not cuckoo.search("false")


def test_delete_false(cuckoo):
    assert cuckoo.delete("test") == False


def test_delete_true(cuckoo):
    cuckoo.insert("test")
    assert cuckoo.search("test")
    assert cuckoo.delete("test")
