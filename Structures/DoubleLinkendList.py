from Structures.Node import DoubleNode


class DoubleLinkedList():

    
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
    
    def addInicio(self, data):
        if self.isEmpty():
            aux = DoubleNode(data, None,None)
            self.head = aux
            self.end = aux
    
        else:
            aux = DoubleNode(data, self.head,None)
            self.head = aux
            self.head.next_node.previous_node = self.head              
        
        self.size+=1
        
        
    def addFin(self, data):
        if self.isEmpty():
            self.addInicio(data)   
        else:
            aux = DoubleNode(data, None, self.end)
            self.end = aux
            self.end.previous_node.next_node = self.end
            self.size+=1

    def reverse(self):
        aux = self.head
        self.clean()
        while aux is not None:
            self.addInicio(aux.data)
            aux = aux.next_node


    def removeHead(self):
        if not self.isEmpty():
            if self.size == 1:
                self.clean()
            
            else:
                aux = self.head.next_node
                self.head = None
                self.head = aux
                self.head.previous_node = None
                self.size -=1

    def removeEnd(self):
        if not self.isEmpty():
            aux = self.end.previous_node
            self.end = None
            if aux == None:
                if self.size == 2:
                    self.end = self.head
                
                else:
                    self.head = None  
            else:
                self.end = None
                self.end = aux
                self.end.next_node = None
            
            self.size-=1
            
    def print(self):
        cont = 0
        messaje = ""

        if self.head is not None:
            temp = self.head
            while temp is not None:
                if cont != 0:
                    messaje +=  " -> "
                    
                messaje += "" + str(temp.data)
                temp = temp.next_node
                cont += 1
            
            print(messaje)
        
        else:
            print("List is empty")
    
    def exist(self, tuple, delete = False):

        if self.head is not None:
            temp = self.head
            data = None
            while temp is not None:
                if temp.data[0] == tuple[0] and temp.data[1] == tuple[1]:
                    data = temp.data
                    break
                temp = temp.next_node

            if(data and delete):
                previous_node = temp.previous_node
                next_node = temp.next_node
                if previous_node == None:
                    self.removeHead()
                elif next_node == None:
                    self.removeEnd()
                else:
                    temp = None
                    previous_node.next_node = next_node
                    next_node.previous_node = previous_node
                    self.size-=1
            return data        
        else:
            return None






    
        