
import graphviz
from Collections.graphic import IGraphable
from Collections.list import IList
from Collections.node import Node


class Queue(IList, IGraphable):
    
    def __init__(self) -> None:
        super().__init__()
    
    def enqueue(self, value):
        new_node = Node(value)
        if self.is_empty():
            self.head = new_node
            self.end = new_node
        else:
            if self.size == 1: self.head.set_next_node(new_node)
            else: self.end.set_next_node(new_node)
            self.end = new_node
        
        self.size += 1
    
    def dequeue(self):
        if self.is_empty(): return None
        removed_node = self.head
        new_head = self.head.get_next_node()
        self.head = None
        self.head = new_head
        self.size -= 1
        if self.is_empty(): self.end = None
        return removed_node.get_value()
    
    def print_values(self):
        if self.is_empty(): return print("Queue is empty")
        current_node = self.head
        cont = 0
        messaje = ""
        while current_node is not None:
            if cont != 0: messaje +=  " -> "
            messaje += "" + str(current_node.get_value())
            current_node = current_node.get_next_node()
            cont += 1
        print(messaje)

    def graph(self, file_name: str, directory='/', format='png'):
        dot = graphviz.Digraph(name='Queue', filename=file_name, format=format)
        dot.graph_attr.update({'rankdir': 'LR'})
        list_id = str(hex(id(self)))
        if self.is_empty(): dot.node('null{0}'.format(list_id), '{ null }', { 'shape': 'record' })
        else:
            # Creating nodes
            def create_node(current: Node, _):
                node_id = str(hex(id(current)))
                dot.node('n{0}'.format(node_id), "{ " + str(current.get_value()) + " | }", { 'shape': 'record' })
            self._for_each_node(create_node)
            dot.node('null{0}'.format(list_id), '{ null }', { 'shape': 'record' })

            # Linking nodes
            def linking_node(current: Node, _):
                # Escape because end-node does not have next node
                if current is self.end: return
                # Generate nodes unique ids
                node_id = str(hex(id(current)))
                next_node_id = str(hex(id(current.get_next_node())))
                # Linking current node and next node
                dot.edge('n{0}'.format(node_id), 'n{0}'.format(next_node_id))
            self._for_each_node(linking_node)

            # Linking null pointes
            end_id = str(hex(id(self.end)))
            dot.edge('n{0}'.format(end_id), 'null{0}'.format(list_id))
        # Generate image
        dot.render(directory=directory, view=True)