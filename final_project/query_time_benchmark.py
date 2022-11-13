import gc  # import python garbage collector
import random
import sys

import numpy as np
import pytest
from execution_time import ExecutionTime
from memory_profiler import LogFile, profile

from cuckoo import Cuckoo

# fp=open('memory_profiler.log','w+')


e = ExecutionTime()
n = sys.argv[1]

# @e.timeit   
# @profile(stream=fp)
def make_cuckoo(n):
    return Cuckoo(n+1, 3)

@e.timeit 
# @profile(stream=fp)
def cuckoo_insert_random_numbers(cuckoo,n):
    #insert a set of kmers into the cuckoo
    cuckoo.insert("00001001")
    for i in range(0,n-1):
        cuckoo.insert(str(random.getrandbits(64)))#test with random 64 bit ints

@e.timeit
def search_wrapper(cuckoo,str_to_search):
    cuckoo.search(str_to_search)

cuckoo = make_cuckoo(int(n)+1)
cuckoo_insert_random_numbers(cuckoo,int(n))
search_wrapper(cuckoo,"00001001")

print(e.logtime_data)
print(n, end=",")
print(e.logtime_data['search_wrapper']['total_time'],end = ",")
print(e.logtime_data['cuckoo_insert_random_numbers']['total_time'],end = ",")
print(e.logtime_data['cuckoo_insert_random_numbers']['average_time'])
