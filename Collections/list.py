from Collections.node import Node


class IList:

    def __init__(self) -> None:
        self.head: Node|None = None
        self.end: Node|None = None
        self.size = 0

    def get_head(self) -> Node|None: return self.head

    def get_size(self): return self.size

    def is_empty(self): return self.head == None

    def clear(self):
        self.head = None
        self.end = None
        self.size = 0

    def for_each(self, callbackFn) -> None:
        """Loop through each element in the list
            Parameters:
                - callbackFn: A function to execute for each element in the list.
                    Parameters:
                        - element: The current elemen being processed in the list.
                        - index: The index of the current element being processed in the list.
        """
        if self.is_empty(): return
        if not callable(callbackFn): return
        index = 0
        current_node = self.head
        while current_node is not None:
            callbackFn(current_node.get_value(), index)
            current_node = current_node.get_next_node()
            index += 1
    
    def _for_each_node(self, callbackFn) -> None:
        """Loop through each Nodes in the list
            Parameters:
                - callbackFn: A function to execute for each Node in the list.
                    Parameters:
                        - node: The current Node being processed in the list.
                        - index: The index of the current Node being processed in the list.
        """
        if self.is_empty(): return
        if not callable(callbackFn): return
        index = 0
        current_node = self.head
        while current_node is not None:
            callbackFn(current_node, index)
            current_node = current_node.get_next_node()
            index += 1
    
  