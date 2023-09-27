import graphviz
from Collections.graphic import IGraphable
from Collections.iterator import Iterator
from Collections.list import IList
from Collections.node import Node


class CircularList(IList, IGraphable):

    def __init__(self):
        super().__init__()
        
    def add_first(self, value):
        new_node = Node(value)
        if self.is_empty():
            self.head = new_node
            self.end = new_node
            self.head.set_next_node(self.end)
            self.head.set_previous_node(self.head)
        else:
            new_node.set_next_node(self.head)
            new_node.set_previous_node(self.end)
            self.head = new_node
            self.head.get_next_node().set_previous_node(self.head)
            self.end.set_next_node(self.head)
        
        self.size += 1

    def add_end(self, value):
        if self.is_empty(): self.add_first(value)       
        else:
            new_node = Node(value)
            new_node.set_next_node(self.head)
            new_node.set_previous_node(self.end)
            self.end = new_node
            self.end.get_previous_node().set_next_node(self.end)
            self.head.set_previous_node(self.end)
            self.size += 1
  
    def print_values(self):
        if self.is_empty(): return print("List is empty")
        cont = 0
        messaje = ""
        current_node = self.head
        while current_node.get_next_node() is not self.head:
            if cont != 0: messaje +=  " -> "
            messaje += "" + str(current_node.get_value())
            current_node = current_node.get_next_node()
            cont += 1
        messaje += " -> " + str(self.end.get_value())
        print(messaje)

    def print_values_reverse(self):
        if self.is_empty(): return print("List is empty")
        cont = 0
        messaje = ""
        current_node = self.end
        while current_node.get_previous_node() is not self.end:
            if cont != 0: messaje +=  " -> "
            messaje += "" + str(current_node.get_value())
            current_node = current_node.get_previous_node()
            cont += 1
        messaje += " -> " + str(self.head.get_value())
        print(messaje)

    def includes(self, value):
        if self.is_empty(): return False
        current_node: Node = self.head.get_next_node()
        if self.head.get_value() == value: return True
        
        while current_node is not self.head:
            if current_node.get_value() == value:
                return True
            current_node = current_node.get_next_node()
            
        return False
    
    def get_iterator(self): return Iterator(self)

    def for_each(self, callbackFn) -> None:
        if self.is_empty(): return
        if not callable(callbackFn): return
        index = 0
        current_node = self.head
        while True:
            callbackFn(current_node.get_value(), index)
            current_node = current_node.get_next_node()
            index += 1
            if current_node is self.head: break
    
    def _for_each_node(self, callbackFn) -> None:
        if self.is_empty(): return
        if not callable(callbackFn): return
        index = 0
        current_node = self.head
        while True:
            callbackFn(current_node, index)
            index += 1
            current_node = current_node.get_next_node()
            if current_node is self.head: break

    def graph(self, file_name: str, directory='/', format='png'):
        dot = graphviz.Digraph(name='Doubly Circular List', filename=file_name, format=format, engine='circo')
        list_id = str(hex(id(self)))
        if self.is_empty(): dot.node('null{0}'.format(list_id), '{ null }', { 'shape': 'record' })
        else:
            # Creating nodes
            def create_node(current: Node, index):
                node_id = str(hex(id(current)))
                dot.node('n{0}'.format(node_id), "{ " + str(index) + "|" + str(current.get_value()) + " }", { 'shape': 'record' })
            self._for_each_node(create_node)

            # Linking nodes
            def linking_node(current: Node, _):
                # Generate nodes unique ids
                node_id = str(hex(id(current)))
                next_node_id = str(hex(id(current.get_next_node())))
                # Linking current node and next node
                dot.edge('n{0}'.format(node_id), 'n{0}'.format(next_node_id))
                dot.edge('n{0}'.format(next_node_id), 'n{0}'.format(node_id), None, { 'color': 'blue' })
            self._for_each_node(linking_node)

        # Generate image
        dot.render(directory=directory, view=True)

