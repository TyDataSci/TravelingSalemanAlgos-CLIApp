# HashTable class using chaining.
class HashTable:
    # Assigns all buckets with an empty list.
    def __init__(self, size=100):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        self.length = 0
        for i in range(size):
            self.table.append([])

    def hash_key(self, key):
        return hash(key) % len(self.table)

    # Inserts a new item into the hash table.
    def add(self, key, value):
        # get the bucket where this item will go.
        bucket = self.hash_key(key)
        item = list([key, value])
        # Check if bucket has items
        if self.table[bucket]:
            found = False
            for _item_ in self.table[bucket]:
                if _item_[0] == key:
                    _item_[1] = value
                    found = True
            # If bucket does not have key, add item
            if not found:
                self.table[bucket].append(item)
                self.length += 1
        # If bucket has no items, add item
        else:
            self.table[bucket].append(item)
            self.length += 1

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def get(self, key):
        # get the bucket list where this key would be.
        bucket = self.hash_key(key)
        if self.table[bucket]:
            for _item_ in self.table[bucket]:
                if _item_[0] == key:
                    return _item_[1]
                    # If not found returns None
        print('Not found')
        return None

    # Removes an item with matching key from the hash table.
    def drop(self, key):
        # get the bucket list where this item will be removed from.
        bucket = self.hash_key(key)

        # remove the item from the bucket list if it is present.
        if self.table[bucket]:
            for index, _item_ in enumerate(self.table[bucket]):
                if _item_[0] == key:
                    self.table[bucket].pop(index)
                    print(f'{key} was removed')
                    self.length -= 1
                    return

        # If not found return
        print(f'{key} not found')
        return

    def keys(self):
        keys = []
        for bucket in self.table:
            for item in bucket:
                keys.append(item[0])
        return keys

    def values(self):
        values = []
        for bucket in self.table:
            for item in bucket:
                values.append(item[1])
        return values

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

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.add(key, value)

    def __len__(self):
        return self.length

    def __iter__(self):
        for key in self.keys():
            yield key, self.get(key)