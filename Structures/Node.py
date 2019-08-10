class Node():
    
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node

class DoubleNode():    
    def __init__(self, data, next_node, previous_node):
        self.data = data
        self.next_node = next_node
        self.previous_node = previous_node