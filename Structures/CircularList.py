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
    
    def add(self, data):
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
    
    def print(self):
        
        cont = 0
        messaje = ""

        if self.head is not None:
            aux = self.head
            while aux.next_node is not self.head:
                if cont != 0:
                    messaje +=  " -> "
                    
                messaje += "" + str(aux.data)
                aux = aux.next_node
                cont += 1
            messaje += " ->" + str(self.end.data)
            print(messaje)
        
        else:
            print("List is empty")




cola = CircularList()

cola.add("Menique")
cola.add("azul")
cola.add("Rolasi")
cola.add("armit")
cola.add("Roco")

print("Imprimir lista 1##")
cola.print()


