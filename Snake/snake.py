
import curses
from Collections.doubly_linked_list import DoublyLinkedList
from Collections.stack import Stack
from Game.context import GameContext
from Snake.interfaces import IAffectableSnake
from Snake.items import Item
from Utils.colors import Color
from Utils.coordinate import Coordinate

# SNAKE_BODY = '©'
SNAKE_BODY = '■'

class Snake(IAffectableSnake):
    
    def __init__(self, stdscr, game_context: GameContext, score_stack: Stack) -> None:
        """
        Parameters:
            stdscr (instance of 'curses.window' class from curses library): 
                An object that provides methods and attributes to perform writing and reading operations 
                on the screen, such as printing text, moving the cursor, and responding to keyboard events.
            game_context (instance of 'GameContext' class)
        """
        self.stdscr = stdscr
        self.ctx = game_context
        self.score_stack = score_stack
        self.snake_body = DoublyLinkedList()
        """List of 'Coordinate' instances."""
        self.reset_snake()

    def reset_snake(self):
        self.snake_body.clear()
        self.current_direction = curses.KEY_RIGHT
        self.__is_alive = True
        self.snake_body.add_last(Coordinate(self.ctx.board_origin.x + 42, self.ctx.board_origin.y + 11))
        self.snake_body.add_last(Coordinate(self.ctx.board_origin.x + 41, self.ctx.board_origin.y + 11))
        self.snake_body.add_last(Coordinate(self.ctx.board_origin.x + 40, self.ctx.board_origin.y + 11))

    def set_direction(self, direction):
        """Set the snake's current direction."""
        # Preventing the snake from making a backward movement in relation to its current direction
        if not ((self.current_direction == curses.KEY_RIGHT and direction == curses.KEY_LEFT) or 
            (self.current_direction == curses.KEY_LEFT and direction == curses.KEY_RIGHT) or 
            (self.current_direction == curses.KEY_UP and direction == curses.KEY_DOWN) or
            (self.current_direction == curses.KEY_DOWN and  direction == curses.KEY_UP)):
            self.current_direction = direction
    
    def get_head_position(self) -> Coordinate | None: 
        return self.snake_body.get_first()
    
    def get_snake_size(self) -> int: return self.snake_body.get_size()

    def is_alive(self) -> bool: return self.__is_alive

    def set_is_alive(self, is_alive: bool) -> None: self.__is_alive = is_alive

    def includes(self, coordiante: Coordinate) -> bool: return self.snake_body.includes(coordiante)
    
    def draw_body_coordinate(self, coordinate: Coordinate):
        self.stdscr.addstr(coordinate.y, coordinate.x, SNAKE_BODY, curses.color_pair(Color.GREEN))

    def erase_body_coordinate(self, coordinate: Coordinate):
        self.stdscr.addstr(coordinate.y, coordinate.x, ' ') 

    def display_body(self):
        """Draw the entire body of the snake on the screen."""
        self.snake_body.for_each(lambda coordinate, _: self.draw_body_coordinate(coordinate))
    
    def update_position(self, new_head:Coordinate):
        # Add the new snake's head to the list and print it    
        self.snake_body.add_first(new_head)
        self.draw_body_coordinate(new_head)
        # Remove in the list the snake's end 
        end = self.snake_body.get_last()
        self.snake_body.remove_last()
        self.erase_body_coordinate(end)

    def confirm_new_head(self, next_head):
        """Confirm whether the new head is correct. Returns if there is a collision. """
        # It's checked first for collision before adding the new head.
        exist_collision = self.snake_body.includes(next_head)
        # Updating snake body
        self.update_position(next_head)
        return exist_collision

    def move_right(self) -> bool:
        """The snake moves to the right. Return if there is collision with itself."""
        # Calculating new head
        current_head:Coordinate = self.snake_body.get_first()
        new_position_x = current_head.x + 1
        if new_position_x >= self.ctx.board_end.x:
            new_position_x = self.ctx.board_origin.x + 1
        next_head = Coordinate(new_position_x, current_head.y)
        # Validating collision
        return self.confirm_new_head(next_head)
    
    def move_left(self) -> bool:
        """The snake moves to the left. Return if there is collision with itself."""
        # Calculating new head
        current_head:Coordinate = self.snake_body.get_first()
        new_position_x = current_head.x - 1
        if new_position_x <= self.ctx.board_origin.x:
            new_position_x = self.ctx.board_end.x - 1
        next_head = Coordinate(new_position_x, current_head.y)
        # Validating collision
        return self.confirm_new_head(next_head)
    
    def move_up(self) -> bool:
        """The snake moves up. Return if there is collision with itself."""
        # Calculating new head
        current_head:Coordinate = self.snake_body.get_first()
        new_position_y = current_head.y - 1
        if new_position_y <= self.ctx.board_origin.y:
            new_position_y = self.ctx.board_end.y - 1
        next_head = Coordinate(current_head.x, new_position_y)
        # Validating collision
        return self.confirm_new_head(next_head)
    
    def move_down(self) -> bool:
        """The snake moves up. Return if there is collision with itself."""
        # Calculating new head
        current_head:Coordinate = self.snake_body.get_first()
        new_position_y = current_head.y + 1
        if new_position_y >= self.ctx.board_end.y:
            new_position_y = self.ctx.board_origin.y + 1
        next_head = Coordinate(current_head.x, new_position_y)
        # Validating collision
        return self.confirm_new_head(next_head)
    
    def make_movement(self):
        """Makes a move depending on the current direction of the snake."""
        if self.current_direction == curses.KEY_RIGHT:
            return self.move_right()
        elif self.current_direction == curses.KEY_LEFT:
            return self.move_left()
        elif self.current_direction == curses.KEY_UP:
            return self.move_up()
        elif self.current_direction == curses.KEY_DOWN:
            return self.move_down()
        return False
    
    def reverse_direction(self):
        """Reverses the snake's current direction."""
        self.snake_body.reverse()
        head:Coordinate = self.snake_body.get_first()
        neck:Coordinate = self.snake_body.find_by_index(1)
        if head is None: return
        if neck is None: return
        new_direction = None
        if head.y == neck.y: # The snake is moving on the X axis.
            if head.x > neck.x: new_direction = curses.KEY_RIGHT
            else: new_direction = curses.KEY_LEFT
        elif head.x == neck.x: # The snake is moving on the Y axis.
            if head.y > neck.y: new_direction = curses.KEY_DOWN
            else: new_direction = curses.KEY_UP
        self.current_direction = new_direction

    # Implemented Method
    def increase_length(self, body_elements_to_increase = 1):
        count = 0
        while count < body_elements_to_increase:
            end = self.snake_body.get_last()
            new_coordinate = Coordinate(end.x, end.y)
            self.snake_body.add_last(new_coordinate)
            self.draw_body_coordinate(new_coordinate)
            self.score_stack.push(self.snake_body.get_first())
            count += 1

    # Implemented Method
    def reduce_length(self, body_elements_to_remove = 1):
        count = 0
        while count < body_elements_to_remove:
            if self.snake_body.get_size() <= 3: return
            end = self.snake_body.get_last()
            self.snake_body.remove_last()
            self.erase_body_coordinate(end)
            count += 1
    
    # Implemented Method
    def kill(self) -> None: self.set_is_alive(False)
    
    def consume_item(self, item: Item):
        item.consume(self)