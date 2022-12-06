import hashlib
import math
import numpy as np

# Source: https://medium.com/@meeusdylan/implementing-a-cuckoo-filter-in-go-147a5f1f7a9


class Counting_Cuckoo_Params:

    def __init__(self, n, fp, max_tries=500, b=4, t=2):
        """
        Initializes Cuckoo hash table

        Args:
            n (int): number of elements to store
            fp (float): false positive rate
            b (int): number of entries per bucket
            t (int): number of hash functions

        Returns:
            Cuckoo hash table
        """
        self.b = b  # number of entries per bucket
        self.f = self.fingerprintLength(4, fp)  # fingerprint length in bits
        self.m = self.nextPower(n / fp * 8)  # number of buckets
        self.fp = fp
        self.table = np.empty((self.m, self.b), dtype=f"U{self.f}, f")
        self.max_tries = max_tries
        self.t = t

    def fingerprintLength(self, k, fp):
        """
        Returns fingerprint length in bits
        """
        return max(1, int(math.ceil(math.log(fp, 2) / k)))

    def nextPower(self, i):
        """
        Returns next power of 2 greater than i
        """
        return 1 << int(i - 1).bit_length()

    def fingerprint(self, data):
        """
        Returns fingerprint of data

        Args:
            data (str): data to fingerprint

        Returns:
            int: fingerprint
        """
        hash = hashlib.sha256(data).hexdigest()
        return hash[:self.f]

    def hash(self, data):
        """
        Hashes data using SHA-256

        Args:
            data (str): data to hash

        Returns:
            hashes list(int): hash values
            f (int): fingerprint
        """
        h = data.encode('utf-8')
        f = self.fingerprint(h)
        hashes = [(1, 0)]
        for i in range(1, self.t+1):
            hashes.append((((i+hashes[-1][0] ^ int(hashlib.sha256(
                f.encode('utf-8')).hexdigest(), 16)) % self.m), i))
        return np.array(hashes[1:]), f

    def insert(self, data):
        """
        Inserts key into hash table

        Args:
            key (str): key to insert

        Returns:
            True if key is inserted, False otherwise
        """
        hashes, f = self.hash(data)
        occ = 1
        for _ in range(self.max_tries):
            for h, _ in hashes:
                for i in range(self.b):  # find empty bucket for each hashed bucket
                    if self.table[h][i][1] == 0:
                        self.table[h][i] = (f, occ)
                        return True
                    elif self.table[h][i][0] == f:
                        occ = self.table[h][i][1]
                        self.table[h][i] = (f, 1 + occ)
                        return True
            # no empty bucket found, evict random entry
            h = np.random.choice(hashes)  # pick random hash
            i = np.random.choice(self.b)  # pick random bucket
            (f, occ), self.table[h][i] = self.table[h][i], (f, occ)
            hashes = [1]
            for i in range(1, self.t+1):
                hashes.append((((i+hashes[-1][0] ^ int(hashlib.sha256(
                    f.encode('utf-8')).hexdigest(), 16)) % self.m), i))
            h = np.array(h[1:])

        # cuckoo data structure is full
        raise Exception('Reached max size')

    def search(self, key):
        """
        Looks for key in hash table

        Args:
            key (str): key to search for

        Returns:
            Occurances if found, 0 if not found
        """
        hashes, f = self.hash(key)
        for h in hashes:
            for i in range(len(self.table[h])):
                if self.table[h][i][1] != 0 and self.table[h][i][0] == f:
                    return self.table[h][i][1]
        return 0

    def delete(self, key):
        """
        Deletes key from hash table

        Args:
            key (str): key to delete

        Returns:
            True if key is deleted, False otherwise
        """
        hashes, f = self.hash(key)
        for h in hashes:
            for i in range(len(self.table[h])):
                if self.table[h][i][1] != 0 and self.table[h][i][0] == f:
                    self.table[h][i] = ('', 0)
                    return True
        return False
