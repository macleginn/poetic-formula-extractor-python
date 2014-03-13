class LinkedList:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

        def __len__(self):
            return len(self.data)
    def __init__(self):
        self.head = None
        self.length = 0
    def __len__(self):
        return self.length
    def __str__(self):
        output = ''
        tempNode = self.head
        i = 1
        while i <= self.length:
            output = output + str(tempNode.data) + '\n'
            tempNode = tempNode.next
            i = i + 1
        output = output.strip('\n')
        return output
    __repr__ = __str__
    def __iter__(self):
        return LinkedListIterator(self.head)
    def add(self, data):
        newNode = self.Node(data)
        temp = self.head
        self.head = newNode
        self.head.next = temp
        self.length = self.length + 1
    def get(self):
        if self.length == 0:
            raise ValueError
        returnValue = self.head.data
        self.head = self.head.next
        self.length = self.length - 1
        return returnValue

class LinkedListIterator:
    def __init__(self, node):
        self.current = node
    def __iter__(self):
        return self
    def __next__(self):
        if self.current is None:
            raise StopIteration()
        output = self.current.data
        self.current = self.current.next
        return output

class DoublyLinkedList:
    class Node:
        def __init__(self, data):
            self.data     = data
            self.next     = None
            self.previous = None
        def __len__(self):
            return len(self.data) 
    
    def __init__(self):    
        self.head   = None
        self.tail   = None
        self.length = 0
    
    def __len__(self):
        return self.length

    def add(self, data):
        newNode = self.Node(data)
        if self.length == 0:
            self.head = newNode
            self.tail = newNode
            self.head.next = None
            self.head.previous = None
            self.tail.next = None
            self.tail.previous = None
            self.length += 1
        elif self.length == 1:
            self.tail = newNode
            self.tail.previous = self.head
            self.head.next     = self.tail
            self.length += 1
        else:
            temp = self.tail
            self.tail = newNode
            self.tail.previous = temp
            temp.next = self.tail
            self.length += 1

    def delete(self, node):
        if node.previous == None:
            self.head = node.next
            self.head.previous = None
            self.length -= 1
        elif node.next == None:
            self.tail = node.previous
            self.tail.next = None
            self.length -= 1
        else:
            node.previous.next = node.next
            node.next.previous = node.previous
            self.length -= 1

    def __iter__(self):
        return DoublyLinkedListIterator(self.head)

class DoublyLinkedListIterator:
    def __init__(self, node):
        self.current = node
    def __iter__(self):
        return self
    def __next__(self):
        if self.current is None:
            raise StopIteration()
        output = self.current
        self.current = self.current.next
        return output