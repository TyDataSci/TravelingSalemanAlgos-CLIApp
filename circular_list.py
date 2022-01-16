import node


class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current_node = None

    def append(self, data):
        new_node = node.Node(data)
        if self.head is None:
            self.head = new_node
            self.head.next = new_node
            self.tail = new_node
            self.current_node = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            self.head.prev = self.tail
            self.tail.next = self.head

    def next_stack(self, last_node):
        min_prev = 2 ** 10
        min_next = 2 ** 10
        for i in self.current_node.prev.data:
            if adj.loc[i, last_node] < min_prev:
                min_prev = adj.loc[i, last_node]
        for i in self.current_node.next.data:
            if adj.loc[i, last_node] < min_next:
                min_next = adj.loc[i, last_node]
        if min_prev < min_next:
            self.current_node = self.current_node.prev
            return self.current_node.data
        else:
            self.current_node = self.current_node.next
            return self.current_node.data

    def __iter__(self, start_node='head'):
        starting_points = {'head': self.head, 'tail': self.tail, 'current_node': self.current_node}
        iter_node = starting_points[start_node]
        while True:
            yield iter_node.data
            iter_node = iter_node.next
            if iter_node is starting_points[start_node]:
                break
