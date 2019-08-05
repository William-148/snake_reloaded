class Node():
    
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node

class Queue():
    def __init__(self):
        self.head = None
        self.end = None
        self.size = 0
    
    def isEmpty(self):
        return self.head == None
    
    def clean(self ):
        self.head = None
        self.end = None
        self.size = 0
    
    def enqueue(self, data):
        
        temp = Node(data, None)
        if self.isEmpty():
            self.head = temp
            self.end = temp
        
        else:
            if self.size == 1:
                self.head.next_node = temp
            
            else:
                self.end.next_node = temp
            
            self.end = temp
        
        self.size += 1
    
    def dequeue(self):
        if self.isEmpty():
            return None
        
        remove = self.head
        temp = self.head.next_node
        self.head = None
        self.head = temp
        self.size -= 1
        if self.isEmpty():
            self.end = None
        
        return remove.data
        
    
    def print(self):
        aux = self.head
        cont = 0
        messaje = ""

        if self.head is not None:
            while aux is not None:
                if cont != 0:
                    messaje +=  " -> "
                messaje += "" + str(aux.data)
                aux = aux.next_node
                cont += 1
            print(messaje)
        
        else:
            print("Queue is empty")



    

