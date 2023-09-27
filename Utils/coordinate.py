class Coordinate:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, self.__class__):
            return __value.x == self.x and __value.y == self.y
        return False
    
    def __str__(self) -> str:
        return '(' + str(self.x) + ', ' + str(self.y) + ')'