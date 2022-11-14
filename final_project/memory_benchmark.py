from memory_profiler import profile
from execution_time import ExecutionTime
import pytest
from counting_cuckoo import Counting_Cuckoo
import random
import numpy as np
from memory_profiler import LogFile
import sys
import gc #import python garbage collector
fp=open('memory_profiler.log','w+') #write outpus


def parse_fasta(fh):
    fa = []
    current_short_name = None
    # Part 1: compile list of lines per sequence
    for ln in fh:
        if ln[0] == '>':
            # new name line; remember current sequence's short name
            long_name = ln[1:].rstrip()

        else:
            # append nucleotides to current sequence
            fa.append(ln.rstrip())

    return fa

with open('16mer.fasta') as fh:
    fa = parse_fasta(fh)
    
@profile(stream=fp)
def make_cuckoo(n):#instantiate structure
    return Counting_Cuckoo(n, 3)


@profile(stream=fp)
def cuckoo_insert_random_numbers(cuckoo,n): # insert until cuckoo is full
    #insert a set of kmers into the cuckoo
    
    for i in range(0,n):
        # cuckoo.insert(str(random.getrandbits(64)))#test with random 64 bit ints
        cuckoo.insert(fa[i])


for i in np.arange(0,50000,1000): #iterate over max size of cuckoo
    gc.collect()
    cuckoo = make_cuckoo(int(i)+1)
    cuckoo_insert_random_numbers(cuckoo,int(i))



