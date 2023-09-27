from Collections.list import IList


class Iterator:
    def __init__(self, list: IList):
        self.list = list
        self.current_node = list.get_head()

    def reset(self):
        self.current_node = self.list.get_head()
    
    def get_size(self) -> int: return self.list.get_size()

    def has_current(self): return self.current_node is not None

    def next(self):
        self.current_node = self.current_node.get_next_node() if self.has_current() else None

    def previous(self):
        self.current_node = self.current_node.get_previous_node() if self.has_current() else None

    def get_current_value(self):
        if not self.has_current(): return None
        return self.current_node.get_value()

    def has_next(self):
        if not self.has_current(): return False
        return self.current_node.get_next_node() is not None

    def has_previous(self):
        if not self.has_current(): return False
        return self.current_node.get_previous_node() is not None