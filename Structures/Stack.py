from Structures.Node import Node

class Stack():
    def __init__(self):
        self.head = None
        self.end  = None
        self.size = 0
    
    def isEmpty(self):
        return self.head == None
    
    def clean(self ):
        self.head = None
        self.end = None
        self.size = 0
    
    def pop(self):
        if self.isEmpty():
            return None
        else:
            if self.size == 1:
                delete_node = self.head
                self.clean()
                return delete_node.data
            else:
                data = self.head.data
                temp = self.head.next_node
                self.head = None
                self.head = temp
                self.size -= 1
                return data

    def push(self, data):
        temp = None
        if self.isEmpty():
            temp = Node (data, None)
            self.head = temp
            self.end = temp
        
        else:
            temp = Node (data, self.head)
            self.head = temp
        
        self.size += 1


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
            print("Stack is empty")

        




