
from Snake.interfaces import IAffectableSnake, IItemType
from Utils.colors import Color
from Utils.coordinate import Coordinate

# Strategy Context Class
class Item:
    def __init__(self, effect: IItemType, position: Coordinate) -> None:
        self.__effect = effect
        self.__position = position
    
    def get_position(self) -> Coordinate:
        return self.__position
    
    def get_color(self) -> int: return self.__effect.color
    
    def consume(self, snake: IAffectableSnake):
        self.__effect.applyEffect(snake)

    def __str__(self) -> str:
        return self.__effect.appearance
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Coordinate):
            return __value.x == self.__position.x and __value.y == self.__position.y
        return False

# Strategy 1
class HeartItem(IItemType):
    def __init__(self) -> None:
        super().__init__()
        self.appearance = '❤️'
        # self.appearance = '¤'
        self.color = Color.RED

    def applyEffect(self, snake: IAffectableSnake):
        snake.increase_length()

# Strategy 2
class MushroomItem(IItemType):
    def __init__(self) -> None:
        super().__init__()
        self.appearance = '🍄'
        # self.appearance = 'Ç'
        self.color = Color.MAGENTA

    def applyEffect(self, snake: IAffectableSnake):
        snake.increase_length(2)

# Strategy 3
class LizardItem(IItemType):
    def __init__(self) -> None:
        super().__init__()
        self.appearance = '🦎'
        # self.appearance = 'Ø'
        # self.appearance = '×'
        self.color = Color.YELLOW

    def applyEffect(self, snake: IAffectableSnake):
        snake.reduce_length()

# Strategy 4
class SkullItem(IItemType):
    def __init__(self) -> None:
        super().__init__()
        self.appearance = '💀'
        # self.appearance = '▒'

    def applyEffect(self, snake: IAffectableSnake):
        snake.kill()