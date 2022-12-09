# Source: https://www.geeksforgeeks.org/counting-bloom-filters-introduction-and-implementation/

import math
from fnvhash import fnv1a_32
from bitarray import bitarray
from bitarray.util import ba2int, int2ba


class CBloomFilter():

    def __init__(self, n, Counter_size=10, bucket_size=4, no_hashfn=200):
        """
        Initializes Counting Bloom Filter
        """

        self.n = n                # number of items to add
        self.N = Counter_size     # size of each counter
        self.m = bucket_size      # total number of the buckets
        self.k = no_hashfn        # number of hash functions

        self.bit_array = []
        for i in range(self.m):
            count = bitarray(self.N)
            count.setall(0)
            self.bit_array.append(count)

    def hash(self, item, seed):
  
        return fnv1a_32(item.encode(), seed) % self.m

    def insert(self, item):
        """
        Hashes data

        Args:
            data (str): data to hash

        Returns:
            int: hash value
        """
        for i in range(self.k):
            index = self.hash(item, i)

            cur_val = ba2int(self.bit_array[index])
            print("cur_value during insert",cur_val)
            new_array = int2ba(cur_val+1, length=self.N)

            self.bit_array[index] = new_array
    def search(self, item):
        """
        Looks for key in hash table
@@ -56,34 +57,31 @@ def search(self, item):
        """
        
        min_counter = float('inf')
        for i in range(self.k):

            index = self.hash(item, i)
            cur_val = ba2int(self.bit_array[index])
            print("item",item)
            print("cur_val",cur_val)
            print("index",index) 
           
            if (not cur_val > 0):
                return 0

            if cur_val < min_counter:
                min_counter = cur_val

        print("min_counter ",min_counter)
        return min_counter
        # count = 0
        # for i in range(self.k):
        #     index = self.hash(item, i)
        #     cur_val = ba2int(self.bit_array[index])
        #     print(item)
        #     print(cur_val)
        #     print(index)       
        #     if cur_val > 0:
        #         count += 1

        # return count


    def delete(self, item):
        """
        Deletes key from hash table

        Args:
            key (str): key to delete
        """
        if (self.search(item)):
            for i in range(self.k):
                index = self.hash(item, i)

                cur_val = ba2int(self.bit_array[index])
                new_array = int2ba(cur_val-1, length=self.N)
                self.bit_array[index] = new_array

            print('Element Removed')
        else:
            print('Element is probably not exist')
    
    def get_count(self, item):
        count = 0
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest]:
                count += 1
        return count

