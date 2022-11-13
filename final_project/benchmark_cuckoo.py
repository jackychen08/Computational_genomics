from memory_profiler import profile
from execution_time import ExecutionTime
import pytest
from cuckoo import Cuckoo
import random
import numpy as np
from memory_profiler import LogFile
import sys
import gc #import python garbage collector
fp=open('memory_profiler.log','w+')


e = ExecutionTime()
n = sys.argv[1]

 
# @profile(stream=fp)
def make_cuckoo(n):
    return Cuckoo(n, 3)

@e.timeit
# @profile(stream=fp)
def cuckoo_insert_random_numbers(cuckoo,n):
    #insert a set of kmers into the cuckoo
    
    for i in range(0,n):
        cuckoo.insert(str(random.getrandbits(64)))#test with random 64 bit ints



cuckoo = make_cuckoo(int(n)+1)
cuckoo_insert_random_numbers(cuckoo,int(n))

print("n is " + n,end=" ")
print(e.logtime_data)

