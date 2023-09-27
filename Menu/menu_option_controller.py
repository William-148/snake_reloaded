

class MenuOptionController:

    def __init__(self, total_options: int, init_option: int = 0) -> None:
        self.__total_options = total_options
        self.__selected_option = init_option
    
    def get_selected_option(self) -> int: return self.__selected_option

    def next_option(self):
        self.__selected_option += 1
        if self.__selected_option > self.__total_options:
            self.__selected_option = 0

    def previous_option(self):
        self.__selected_option -= 1
        if self.__selected_option < 0:
            self.__selected_option = self.__total_options