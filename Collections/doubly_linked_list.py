import graphviz
from Collections.graphic import IGraphable
from Collections.list import IList
from Collections.node import Node

class DoublyLinkedList(IList, IGraphable):

    def __init__(self) -> None:
        super().__init__()
    
    def get_first(self):
        if not self.is_empty():
            return self.head.get_value()
        return None
    
    def get_last(self):
        if not self.is_empty():
            return self.end.get_value()
        return None
    
    def find_by_index(self, index):
        current_node = self.head
        count = 0
        while current_node is not None and count < index:
            current_node = current_node.get_next_node()
            count = count + 1
        if current_node is None: return None
        return current_node.get_value()
    
    def add_first(self, value):
        first_node = Node(value)
        if self.is_empty():
            self.head = first_node
            self.end = first_node
        else:
            second_node = self.head
            first_node.set_next_node(second_node)
            second_node.set_previous_node(first_node)
            self.head = first_node
        
        self.size += 1
        
    def add_last(self, value):
        if self.is_empty(): self.add_first(value)   
        else:
            penultimate_node = self.end
            last_node = Node(value)
            last_node.set_previous_node(penultimate_node)
            penultimate_node.set_next_node(last_node)
            self.end = last_node
            self.size += 1

    def reverse(self):
        # Getting first node to iterate
        current_node = self.head
        # Reversing nodes head and end
        new_last_node = self.head
        new_first_node = self.end
        self.head = new_first_node
        self.end = new_last_node
        # Reversing pointers of all nodes
        while current_node is not None:
            # Getting current node pointers
            next_node = current_node.get_next_node()
            previous_node = current_node.get_previous_node()
            # Reverse current node pointers
            current_node.set_next_node(previous_node)
            current_node.set_previous_node(next_node)
            # Changing to the next node
            current_node = next_node
        
    def remove_first(self):
        if not self.is_empty():
            if self.get_size() == 1:
                self.clear()
            else:
                first_node = self.head.get_next_node()
                first_node.set_previous_node(None)
                self.head = None
                self.head = first_node
                self.size -= 1

    def remove_last(self):
        if self.is_empty(): return
        last_node = self.end.get_previous_node()
        self.end = None
        if last_node is None:
            self.head = None  
        else:
            self.end = last_node
            self.end.set_next_node(None)
        
        self.size -= 1
            
    def print_values(self):
        if self.is_empty(): return print("List is empty")
        cont = 0
        messaje = ""
        current_node = self.head
        while current_node is not None:
            if cont != 0: messaje +=  " -> "
            messaje += "" + str(current_node.get_value())
            current_node = current_node.get_next_node()
            cont += 1
        print(messaje)
            

    def includes(self, value):
        if self.is_empty(): return False
        current_node = self.head
        while current_node is not None:
            if current_node.get_value() == value:
                return True
            current_node = current_node.get_next_node()
        return False
    
    def pop_if_exist(self, value):
        if self.is_empty(): return None
        current_node = self.head
        finded = False
        value_finded = None
        while current_node is not None:
            if current_node.get_value() == value:
                value_finded = current_node.get_value()
                finded = True
                break
            current_node = current_node.get_next_node()

        if finded:
            previous_node = current_node.get_previous_node()
            next_node = current_node.get_next_node()
            if previous_node is None:
                self.remove_first()
            elif next_node is None:
                self.remove_last()
            else:
                current_node = None
                previous_node.set_next_node(next_node)
                next_node.set_previous_node(previous_node)
                self.size -= 1
        return value_finded

    def graph(self, file_name: str, directory = '/', format='png'):
        dot = graphviz.Digraph(name='Doubly Liked List', filename=file_name, format=format)
        dot.graph_attr.update({'rankdir': 'LR'})
        list_id = str(hex(id(self)))
        if self.is_empty(): dot.node('nullA{0}'.format(list_id), '{ null }', { 'shape': 'record' })
        else:
            # Creating nodes
            def create_node(current: Node, _):
                node_id = str(hex(id(current)))
                dot.node('n{0}'.format(node_id), "{ | " + str(current.get_value()) + " | }", { 'shape': 'record' })

            dot.node('nullA{0}'.format(list_id), '{ null }', { 'shape': 'record' })
            self._for_each_node(create_node)
            dot.node('nullB{0}'.format(list_id), '{ null }', { 'shape': 'record' })

            # Linking nodes
            def linking_node(current: Node, _):
                # Escape because end-node does not have next node
                if current is self.end: return 
                # Generate nodes unique ids
                node_id = str(hex(id(current)))
                next_node_id = str(hex(id(current.get_next_node())))
                # Linking current node and next node
                dot.edge('n{0}'.format(node_id), 'n{0}'.format(next_node_id))
                dot.edge('n{0}'.format(next_node_id), 'n{0}'.format(node_id), None, { 'color': 'blue' })
            self._for_each_node(linking_node)

            # Linking null pointes
            head_id = str(hex(id(self.get_head())))
            end_id = str(hex(id(self.end)))
            dot.edge('nullA{0}'.format(list_id), 'n{0}'.format(head_id), None, { 'color': 'white' })
            dot.edge('n{0}'.format(head_id), 'nullA{0}'.format(list_id), None, { 'color': 'blue' })
            dot.edge('n{0}'.format(end_id), 'nullB{0}'.format(list_id))
            
        # Generate image
        dot.render(directory=directory, view=True)
