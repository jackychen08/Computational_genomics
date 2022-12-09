from memory_profiler import profile
from execution_time import ExecutionTime
import pytest
from counting_cuckoo import Counting_Cuckoo
from counting_bloom import CBloomFilter
from cuckoo import Cuckoo
import random
import numpy as np
from memory_profiler import LogFile
import sys
import gc  # import python garbage collector
import pyjellyfish


# max_tries_all = [100, 250, 500, 1000, 2000, 5000]
# b_all = [4, 8, 16, 32, 64, 128]
max_tries = 500
b = 4
# write output
fp_orig = open('Output/memory_profiler_' + str(max_tries) +
               '_' + str(b) + '_orig.log', 'w')
fp_counting = open('Output/memory_profiler_' +
                   str(max_tries) + '_' + str(b) + '_counting.log', 'w')
fp_bloom = open('Output/memory_profiler_' +
                str(max_tries) + '_' + str(b) + '_bloom.log', 'w')
fp_jelly = open('Output/memory_profiler_' +
                str(max_tries) + '_' + str(b) + '_jelly.log', 'w')


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


@profile(stream=fp_counting)
def make_cuckoo_counting(n):  # instantiate structure
    return Counting_Cuckoo(n, 3, max_tries=max_tries, b=b)


@profile(stream=fp_bloom)
def make_cuckoo_bloom(n):  # instantiate structure
    return CBloomFilter(n, b)


# @profile(stream=fp)
# def make_cuckoo_jelly(n):  # instantiate structure
#     cuckoo = pyjellyfish.Jellyfish('16mer.fasta')
#     cuckoo.initialize()
#     return cuckoo


@profile(stream=fp_orig)
def make_cuckoo_counting_orig(n):  # instantiate structure
    return Cuckoo(n, 3, max_tries=max_tries, b=b)


gc.collect()
cuckoo = make_cuckoo_counting(int(50000)+1)
cuckoo = make_cuckoo_bloom(int(50000)+1)
cuckoo = make_cuckoo_counting_orig(int(50000)+1)
# cuckoo = make_cuckoo_jelly(int(50000)+1)
