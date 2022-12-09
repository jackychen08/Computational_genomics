# Adapted from https://medium.com/analytics-vidhya/cbfs-44c66b1b4a78

import math
import hashlib

class CBloomFilter:  # Counting bloom filters class

    def __init__(self, expected_inputS, false_positiveP):

        self.expected_inputS = expected_inputS  # The expected input size (n)
        # The desired false positive proability (p)
        self.false_positiveP = false_positiveP

        # Finding the array size (m) from the function
        self.size = round((self.expected_inputS *
                             math.log(self.false_positiveP)) / (math.log(2))**2)
        self.array = [0] * self.size  # Creating a list of zeros with size m

        # Finding the optimal number of hashing functions
        self.hashing_n = round(
            (self.size / self.expected_inputS) * math.log(2))

        # Check if the number of hashing funcitons is greater than 6 or less than one
        # So, the number of hashing functions stays in the bounderies between 1 and 6
        if (self.hashing_n > 6):
            self.hashing_n = 6
        elif (self.hashing_n < 1):
            self.hashing_n = 1

    def hashing(self, element):  # Define the hash functions
        keys = []  # That list will the keys for the element
        # Use the first hash function
        hash_object1 = hashlib.md5(element.encode())
        # Use the second hash function
        hash_object2 = hashlib.sha1(element.encode())
        # Use the third hash function
        hash_object3 = hashlib.sha224(element.encode())
        # Use the fourth hash function
        hash_object4 = hashlib.sha256(element.encode())
        # Use the fifth hash function
        hash_object5 = hashlib.sha384(element.encode())
        # Use the sixth hash function
        hash_object6 = hashlib.sha512(element.encode())
        # Append the keys into the list
        keys.append(int(hash_object1.hexdigest(), 16))
        keys.append(int(hash_object2.hexdigest(), 16))
        keys.append(int(hash_object3.hexdigest(), 16))
        keys.append(int(hash_object4.hexdigest(), 16))
        keys.append(int(hash_object5.hexdigest(), 16))
        keys.append(int(hash_object6.hexdigest(), 16))
        return keys  # Return the list of keys

    def insert(self, element):  # use the Add method to add elements into the array

        keys = self.hashing(element)  # Find the hashing keys for the element
        key = 0  # Reset the current key

        # Loop through the every key in the list up to the limit
        for indx in range(self.hashing_n):
            # Find the key moduls from the list size
            key = int(math.fmod(keys[indx], self.size))
            self.array[key] += 1  # Increase the counter value by one
          
        return True

    def delete(self, element):  # use the Remove method to remove elements from the lists

        keys = self.hashing(element)  # Find the hashing keys for the element
        key = 0  # Reset the current key

        if (self.search(element) > 0):  # Check if that element in the list or not
            # Loop through the every key in the list up to the limit
            for indx in range(self.hashing_n):
                # Find the key moduls from the list size
                key = int(math.fmod(keys[indx], self.size))
                # Decrease the counter value by one
                self.array[key] = self.array[key] - 1
            return True

        else: 
          return False
        
    def search(self, element): #Checks if an element is in the data structure or not
        keys = self.hashing (element) #Find the keys for the elements 
        key = 0 #Reset the current key
        
        min_counter = float('inf')
        for indx in range (self.hashing_n): #Loop through the every key in the list up to the limit
            key = int(math.fmod(keys[indx], self.size))#Find the key moduls from the list size
            cur_val = self.array[key]
            if (not cur_val > 0):
                return 0

            if cur_val < min_counter:
                min_counter = cur_val

        return min_counter
