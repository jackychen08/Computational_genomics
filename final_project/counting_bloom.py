#Source: https://www.geeksforgeeks.org/counting-bloom-filters-introduction-and-implementation/

import math
from fnvhash import fnv1a_32
from bitarray import bitarray
from bitarray.util import ba2int,int2ba
 
class CBloomFilter():

    def __init__(self, n,Counter_size,bucket_size,no_hashfn):
        """
        Initializes Counting Bloom Filter
        """
 
        self.n=n                # number of items to add
        self.N=Counter_size     # size of each counter
        self.m=bucket_size      # total number of the buckets
        self.k=no_hashfn        # number of hash functions

        self.bit_array = []
        for i in range(self.m):
            count=bitarray(self.N)
            count.setall(0)
            self.bit_array.append(count)
 
    def hash(self, item, seed):
        return fnv1a_32(item.encode(),seed) % self.m
 
    def insert(self, item):
        """
        Hashes data

        Args:
            data (str): data to hash

        Returns:
            int: hash value
        """
        for i in range(self.k):
            index = self.hash(item,i)
 
            cur_val=ba2int(self.bit_array[index])
            new_array=int2ba(cur_val+1,length=self.N)
             
            self.bit_array[index]=new_array
    
    def search(self, item):
        """
        Looks for key in hash table

        Args:
            key (str): key to search for

        Returns:
            True if key is found, False otherwise
        """
        min = float('inf')
        for i in range(self.k):
            index = self.hash(item,i)
            cur_val=ba2int(self.bit_array[index])

            if(not cur_val > 0):
                return 0

            if cur_val < min:
                    min = cur_val
        return min
       
    def delete(self,item):
        """
        Deletes key from hash table

        Args:
            key (str): key to delete
        """
        if(self.search(item)):
            for i in range(self.k):
                index = self.hash(item,i)
                 
                cur_val=ba2int(self.bit_array[index])
                new_array=int2ba(cur_val-1,length=self.N)
                self.bit_array[index]=new_array
 
            print('Element Removed')
        else:
            print('Element is probably not exist')


    