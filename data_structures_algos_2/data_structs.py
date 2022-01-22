# HashTable class using chaining.
class HashTable:
    def __init__(self, size=100):
        self.table = []
        self.length = 0
        for i in range(size):
            self.table.append([])

    def hash_key(self, key):
        return hash(key) % len(self.table)

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

    def get(self, key):
        bucket = self.hash_key(key)
        if self.table[bucket]:
            for _item_ in self.table[bucket]:
                if _item_[0] == key:
                    return _item_[1]
        print('Not found')
        return None

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


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.head.next = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            self.head.prev = self.tail
            self.tail.next = self.head

    def __iter__(self):
        iter_node = self.head
        while True:
            yield iter_node.data
            iter_node = iter_node.next
            if iter_node is self.head:
                break
