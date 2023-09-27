class Node:

    def __init__(self, value) -> None:
        self.__value = value
        self.__next_node = None
        self.__previous_node = None

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def set_next_node(self, next_node):
        self.__next_node = next_node

    def get_next_node(self):
        return self.__next_node
    
    def set_previous_node(self, previous_node):
        self.__previous_node = previous_node

    def get_previous_node(self):
        return self.__previous_node
    
    def __str__(self) -> str:
        return str(self.__value)

