class Cuckoo:

    def __init__(self, size, num_hash):
        """
        Initializes Cuckoo hash table

        Args:
            size (int): size of the hash table
            num_hash (int): max number of iterations before rehashing

        Returns:
            Cuckoo: Cuckoo hash table
        """
        self.size = size
        self.num_keys = 0
        self.rehash = 1
        self.num_hash = num_hash
        self.hash_table = [[None] * size, [None] * size]

    def hash(self, key, table):
        """
        Hashes key using table

        Args:
            key (str): key to hash
            table (int): which hash table to use

        Returns:
            int: index of hash table
        """
        # TODO: update hashing function
        if table == 0:
            return key ** self.rehash % self.size
        else:
            return (key ** self.rehash // self.size) % self.size

    def rehash(self):
        """
        Rehash all existing keys
        """
        self.rehash += 1
        keys = [k for k in self.hash_table[0] if k != None] + \
            [k for k in self.hash_table[1] if k != None]
        self.hash_table = [[None] * self.size, [None] * self.size]
        for k in keys:
            self.insert(k)

    def insert(self, key):
        """
        Inserts key into hash table

        Args:
            key (str): key to insert

        Returns:
            True if key is inserted, False otherwise
        """
        table_idx = 0
        if self.num_keys + 1 > self.size:  # cannot insert because table is full
            return False
        for _ in range(self.num_hash):
            index = self.hash(key, table_idx)
            if self.table[table_idx][index] == None:  # empty slot
                self.hash_table[index] = key
                self.num_keys += 1
                return True
            else:  # swap
                temp = self.hash_table[table_idx][index]
                self.hash_table[index] = key
                key = temp
                table_idx = 1 - table_idx
        self.rehash()  # rehash all existing keys
        self.insert(key)

    def search(self, key):
        """
        Looks for key in hash table

        Args:
            key (str): key to search for

        Returns:
            True if key is in hash table, False otherwise
        """
        for i in range(2):
            index = self.hash(key, i)
            if self.hash_table[i][index] == key:
                return True
        return False

    def delete(self, key):
        """
        Deletes key from hash table

        Args:
            key (str): key to delete

        Returns:
            True if key is deleted, False otherwise
        """
        for i in range(2):
            index = self.hash(key, i)
            if self.hash_table[i][index] == key:
                self.hash_table[i][index] = None
                return True
        return False
