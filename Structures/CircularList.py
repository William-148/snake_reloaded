
class Node():
    
    def __init__(self, data, next_node, previous_node):
        self.data = data
        self.next_node = next_node
        self.previous_node = previous_node


class CircularList():
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
    
    def addFirst(self, data):
        if self.isEmpty():
            temp = Node(data,None,None)
            self.head = temp
            self.end = temp
            self.head.next_node = self.end
            self.head.previous_node = self.head
        
        else:
            temp = Node(data, self.head,self.end)
            self.head = temp
            self.head.next_node.previous_node = self.head
            self.end.next_node = self.head           
        
        self.size += 1

    def addEnd(self, data):
        if self.isEmpty():
            self.addFirst(data)       
        else:
            temp = Node(data, self.head, self.end)
            self.end = temp
            self.end.previous_node.next_node = self.end
            self.head.previous_node = self.end
            self.size += 1
        
    def printInicioFin(self):
        temp = self.head
        while temp is not None:
            print(str(temp.data))
            temp = temp.next_node
            
    def getList(self):
        return self.head



    def print(self):
        
        cont = 0
        messaje = ""

        if self.head is not None:
            temp = self.head
            while temp.next_node is not self.head:
                if cont != 0:
                    messaje +=  " -> "
                    
                messaje += "" + str(temp.data)
                temp = temp.next_node
                cont += 1
            messaje += " -> " + str(self.end.data)
            print(messaje)
        
        else:
            print("List is empty")


