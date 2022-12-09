import gc  # import python garbage collector
import random
import sys

import numpy as np
import pytest
from execution_time import ExecutionTime
from memory_profiler import LogFile, profile
from counting_cuckoo import Counting_Cuckoo


# fp=open('memory_profiler.log','w+')
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

<<<<<<< Updated upstream
with open('data/mer_counts_dumps.fa') as fh:
=======

with open('16mer.fasta') as fh:
>>>>>>> Stashed changes
    fa = parse_fasta(fh)

e = ExecutionTime()
n = sys.argv[1]

# @e.timeit
# @profile(stream=fp)


<<<<<<< Updated upstream
# @profile(stream=fp)
def cuckoo_insert_random_numbers(cuckoo,n):
    #insert a set of kmers into the cuckoo
    for i in range(0,n-2):
        cuckoo.insert(fa[i])#test with a lenght 16 kmer bit ints
    cuckoo_insert_last_num(cuckoo,n) # test how much time it takes to insert the last file

@e.timeit
def cuckoo_insert_last_num(cuckoo,n):
    cuckoo.insert(fa[n-1])

@e.timeit
def search_wrapper(cuckoo,n):
    cuckoo.search(fa[i])#test with a lenght 16 kmer bit ints

cuckoo = make_cuckoo(int(n)+2)
cuckoo_insert_random_numbers(cuckoo,int(n))
for i in range(0,int(n)-2):
    search_wrapper(cuckoo,fa[i])


print(n, end=",")
print(e.logtime_data['search_wrapper']['average_time'],end = ",")
print(e.logtime_data['cuckoo_insert_last_num']['total_time'],end = ",")
print(e.logtime_data['cuckoo_insert_last_num']['average_time'])
=======
def make_cuckoo(n):
    max_tries = [100, 250, 500, 1000, 2000, 5000]
    b = [4, 8, 16, 32, 64, 128]
    return Counting_Cuckoo(n+1, 3, max_tries=max_tries[0], b=b[0])


@e.timeit
# @profile(stream=fp)
def cuckoo_insert_random_numbers(cuckoo, n):
    # insert a set of kmers into the cuckoo
    for i in range(0, n-1):
        cuckoo.insert(fa[i])  # test with a lenght 16 kmer bit ints


@e.timeit
def search_wrapper(cuckoo, str_to_search):
    cuckoo.search(str_to_search)


cuckoo = make_cuckoo(int(n)+1)
cuckoo_insert_random_numbers(cuckoo, int(n))
search_wrapper(cuckoo, fa[0])


print(n, end=",")
print(e.logtime_data['search_wrapper']['total_time'], end=",")
print(e.logtime_data['cuckoo_insert_random_numbers']['total_time'], end=",")
print(e.logtime_data['cuckoo_insert_random_numbers']['average_time'])
>>>>>>> Stashed changes
