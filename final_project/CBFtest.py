import pytest
from counting_bloom import CBloomFilter

 
@pytest.fixture

def cb():
    return CBloomFilter(500, 3)


def test_insert(cb):
    assert cb.insert("test")
    assert cb.search("test")


def test_insert_full(cb):
    for i in range(4364):
        assert cb.insert(str(i))
    for i in range(4364):
        assert cb.search(str(i))


def test_not_there(cb):
    assert not cb.search("false")

def test_delete_false(cb):
    assert cb.delete("test") == False
    
def test_delete_true(cb):
    cb.insert("test")
    assert cb.delete("test")


# if __name__=="__main__": 
#     test_delete_true(CBloomFilter(500, 3, 20, 2))