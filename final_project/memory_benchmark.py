from memory_profiler import profile
from execution_time import ExecutionTime
import pytest
from cuckoo import Cuckoo
import random
import numpy as np
from memory_profiler import LogFile
import sys
import gc #import python garbage collector
fp=open('memory_profiler.log','w+') #write outpus

@profile(stream=fp)
def make_cuckoo(n):#instantiate structure
    return Cuckoo(n, 3)


@profile(stream=fp)
def cuckoo_insert_random_numbers(cuckoo,n): # insert until cuckoo is full
    #insert a set of kmers into the cuckoo
    
    for i in range(0,n):
        cuckoo.insert(str(random.getrandbits(64)))#test with random 64 bit ints


for i in np.arange(0,1000000,10000): #iterate over max size of cuckoo
    gc.collect()
    cuckoo = make_cuckoo(int(i)+1)
    cuckoo_insert_random_numbers(cuckoo,int(i))



