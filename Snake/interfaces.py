from Utils.colors import Color

class IAffectableSnake:

    def increase_length(self, body_elements_to_increase) -> None:
        pass

    def reduce_length(self, body_elements_to_remove) -> None:
        pass
    
    def kill(self) -> None:
        pass


class IItemType:
    def __init__(self) -> None:
        self.appearance:str = ''
        self.color:int = Color.WHITE

    def applyEffect(self, snake:IAffectableSnake) -> None:
        pass

