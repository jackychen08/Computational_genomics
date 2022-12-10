import gc  # import python garbage collector
import random
import sys

import numpy as np
import pytest
from execution_time import ExecutionTime
from memory_profiler import LogFile, profile
from counting_cuckoo import Counting_Cuckoo
from counting_bloom import CBloomFilter
from cuckoo import Cuckoo
import pandas as pd 

e = ExecutionTime()
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


# @e.timeit   
# @profile(stream=fp)
def make_cuckoo(n,max_tries,b,which_filter):

    if which_filter == "counting_cuckoo":
        return Counting_Cuckoo(n+1, 3,max_tries,b)
    elif which_filter == "cuckoo":
        return Cuckoo(n+1,3,max_tries,b)
    elif which_filter =="counting_bloom":
        return CBloomFilter(n+1,3)


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


with open('data/16-mers.fa') as fh:
    fa = parse_fasta(fh)


# df = pd.Dataframe

n = sys.argv[1]
which_filter = sys.argv[2] # options:counting_cuckoo, cuckoo, counting_bloom
max_tries_index = int(sys.argv[3])#max_tries_index
b_index = int(sys.argv[4]) # index for b array


max_tries = [100, 250, 500, 1000, 2000, 5000] # default for max_tries = 500 
b = [4, 8, 16, 32, 64, 128] # default for b is 8. 


cuckoo = make_cuckoo(11190,max_tries[max_tries_index],b[b_index],which_filter) #TODO shouldnt this be 5000 for the first param
cuckoo_insert_random_numbers(cuckoo,int(n))
for i in range(0,int(n)-2):
    search_wrapper(cuckoo,fa[i])

print(which_filter,end=",")
print(n, end=",")
print(max_tries[max_tries_index],end=",")
print(b[b_index],end=",")
print(e.logtime_data['search_wrapper']['average_time'],end = ",")
print(e.logtime_data['cuckoo_insert_last_num']['total_time'],end = ",")
print(e.logtime_data['cuckoo_insert_last_num']['average_time'])
