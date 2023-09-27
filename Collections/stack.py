import graphviz
from Collections.graphic import IGraphable
from Collections.list import IList
from Collections.node import Node

class Stack(IList, IGraphable):

    def __init__(self) -> None:
        super().__init__()
    
    def pop(self):
        if self.is_empty(): return None
        else:
            if self.size == 1:
                delete_node = self.head
                self.clear()
                return delete_node.get_value()
            else:
                value = self.head.get_value()
                new_head = self.head.get_next_node()
                self.head = None
                self.head = new_head
                self.size -= 1
                return value
    
    def push(self, value):
        new_node = Node(value)
        if self.is_empty():
            self.head = new_node
        else:
            new_node.set_next_node(self.head)
            self.head = new_node
        
        self.size += 1

    def print_values(self):
        if self.is_empty(): return print("Stack is empty")
        aux = self.head
        cont = 0
        messaje = ""
        while aux is not None:
            if cont != 0: messaje +=  " -> "
            messaje += "" + str(aux.get_value())
            aux = aux.get_next_node()
            cont += 1
        print(messaje)

    def graph(self, file_name: str, directory = '/', format='png'):
        dot = graphviz.Digraph(name='Stack', filename=file_name, format=format)
        list_id = str(hex(id(self)))
        if self.is_empty(): dot.node('nullA{0}'.format(list_id), '{ null }', { 'shape': 'record' })
        else:
            label = ""
            current_node = self.get_head()
            while current_node is not None:
                label += " |" + str(current_node)
                current_node = current_node.get_next_node()

            dot.node('n{0}'.format(list_id), "{" + label + "}", { 'shape': 'record' })
        # Generate image
        dot.render(directory=directory, view=True)
        