# HashTable class using chaining.
class HashTable:
    def __init__(self, size=100):
        self.table = []
        self.length = 0
        for i in range(size):
            self.table.append([])

    # Returns key as hash modulus the size of table whose default size is 100 --> O(1)
    def hash_key(self, key):
        return hash(key) % len(self.table)

    # Adds key and value to bucket using chaining insertion. If key exists updates value --> O(1)
    def add(self, key, value):
        bucket = self.hash_key(key)
        item = list([key, value])
        if self.table[bucket]:
            found = False
            for _item_ in self.table[bucket]:
                if _item_[0] == key:
                    _item_[1] = value
                    found = True
            if not found:
                self.table[bucket].append(item)
                self.length += 1
        else:
            self.table[bucket].append(item)
            self.length += 1

    # retrieves value using key hash function. Chained list will iterate to find key --> O(1)
    def get(self, key):
        bucket = self.hash_key(key)
        if self.table[bucket]:
            for _item_ in self.table[bucket]:
                if _item_[0] == key:
                    return _item_[1]
        print('Not found')
        return None

    # Removes key value from hash table return key removed. If not found returns key not found. --> O(1)
    def drop(self, key):
        bucket = self.hash_key(key)

        if self.table[bucket]:
            for index, _item_ in enumerate(self.table[bucket]):
                if _item_[0] == key:
                    self.table[bucket].pop(index)
                    print(f'{key} was removed')
                    self.length -= 1
                    return
        print(f'{key} not found')
        return

    # Iterates through all buckets and keys. Returns all keys in table --> O(n)
    def keys(self):
        keys = []
        for bucket in self.table:
            for item in bucket:
                keys.append(item[0])
        return keys

    # Iterates through all buckets and keys. Returns all values in a table --> O(n)
    def values(self):
        values = []
        for bucket in self.table:
            for item in bucket:
                values.append(item[1])
        return values

    # String converts hash table in a very similar manner to how dictionaries are display on print. --> O(n)
    def __str__(self):
        keys = self.keys()
        values = self.values()
        table_to_str = '{'
        for i in range(len(self.keys())):
            table_to_str += f"{repr(keys[i])}: "
            table_to_str += repr(values[i])
            if i != len(self.keys()) - 1:
                table_to_str += ', ' + '\n'
            else:
                table_to_str += '}'
        return str(table_to_str)

    # Overloads [] method and allows the use of square bracket retrieval --> O(1)
    def __getitem__(self, key):
        return self.get(key)

    # Overloads [] method and allows the use of square bracket to add [key] = value --> O(1)
    def __setitem__(self, key, value):
        self.add(key, value)

    # Returns length of keys in hash table --> O(1)
    def __len__(self):
        return self.length

    # Iterates through all keys and displays as key,value --> O(n)
    def __iter__(self):
        for key in self.keys():
            yield key, self.get(key)
