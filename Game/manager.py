import curses
import random
from Snake.items import HeartItem, Item, LizardItem, MushroomItem, SkullItem
from Collections.doubly_linked_list import DoublyLinkedList
from Utils.coordinate import Coordinate
from Game.context import GameContext
from Collections.stack import Stack
from Utils.colors import Color
from Snake.snake import Snake

MAX_SCORE_PER_LEVEL = 30
SPEED_INIT = 160
SPEED_PLUS = 5

class GameStatus:
    ON_GOING = 1
    GAME_OVER = 2

class GameManager:

    def __init__(self, stdscr, game_context: GameContext) -> None:
        """
        Parameters:
            stdscr (instance of 'curses.window' class from curses library): 
                An object that provides methods and attributes to perform writing and reading operations 
                on the screen, such as printing text, moving the cursor, and responding to keyboard events.
            game_context (instance of 'GameContext' class)
        """
        self.stdscr = stdscr
        self.ctx = game_context
        self.game_status = GameStatus.ON_GOING
        self.speed_level = SPEED_INIT
        self.current_level = 1
        self.score_stack = Stack()
        self.items_score_list = DoublyLinkedList()
        self.snake = Snake(stdscr, game_context, self.score_stack)


    def get_random_coordinate(self) -> Coordinate:
        """Generate a random coordinate within the boundaries of the game board."""
        return Coordinate(
            random.randint(self.ctx.board_origin.x + 1, self.ctx.board_end.x - 1),
            random.randint(self.ctx.board_origin.y + 1, self.ctx.board_end.y - 1)
        )
    
    def delay(self, time:int):
        self.stdscr.timeout(time)
        self.stdscr.getch()            
        self.stdscr.timeout(self.speed_level)
    
    def get_coordinate_without_collision(self) -> Coordinate | None:
        coordinate = None
        count = 0
        while coordinate is None:
            coordinate = self.get_random_coordinate()
            if self.snake.includes(coordinate) or self.items_score_list.includes(coordinate):
                coordinate = None
            if count > 1000: break
            count += 1
        return coordinate

    def level_up(self):
        self.current_level += 1
        self.score_stack.clear()
        # When the level is lower, the snake will go faster
        self.speed_level -= SPEED_PLUS

    def create_food(self):
        coordinate = self.get_coordinate_without_collision()
        if coordinate is None: return
        new_food = None
        random_number = random.randint(0,99)
        if random_number < 10:
            new_food = Item(MushroomItem(), coordinate)
        else:
            new_food = (Item(HeartItem(), coordinate))
        self.items_score_list.add_last(new_food)
        return new_food
    
    def create_wall(self):
        coordinate = self.get_coordinate_without_collision()
        if coordinate is None: return
        new_wall = Item(SkullItem(), coordinate)
        self.items_score_list.add_last(new_wall)
        return new_wall
    
    def create_food_obstacle(self):
        coordinate = self.get_coordinate_without_collision()
        if coordinate is None: return
        random_number = random.randint(0,99)
        new_food = None
        if random_number < 10:
            new_food = Item(SkullItem(), coordinate)
        elif random_number < 40:
            new_food = Item(LizardItem(), coordinate)
        if new_food is not None: self.items_score_list.add_last(new_food)
        return new_food

    def display_new_food(self):
        """Creates a new food and displays it on the screen."""
        new_food = self.create_food()
        new_obstacle = self.create_food_obstacle()
        self.stdscr.addstr(new_food.get_position().y, new_food.get_position().x, str(new_food), curses.color_pair(new_food.get_color()))
        if new_obstacle is not None: 
            self.stdscr.addstr(new_obstacle.get_position().y, new_obstacle.get_position().x, str(new_obstacle), curses.color_pair(new_obstacle.get_color()))

    def display_new_wall(self):
        """Creates a new wall and displays it on the screen."""
        new_wall = self.create_wall()
        self.stdscr.addstr(new_wall.get_position().y, new_wall.get_position().x, str(new_wall))
    
    def display_list_score_items(self):
        """Displays all items (foods and walls) on the screen."""
        self.items_score_list.for_each(lambda item, _: (
            self.stdscr.addstr(item.get_position().y, item.get_position().x, str(item))
        ))
    
    def display_header_game(self):
        origin_x, origin_y = self.ctx.get_game_board_origin()
        # Print score
        score_txt = " Score : " + str(self.score_stack.get_size()) + " "
        self.stdscr.addstr(origin_y, origin_x + 2, score_txt, curses.color_pair(Color.CYAN))

        # Print Level
        leveltxt = " SNAKE RELOADED | LEVEL : " + str(self.current_level) + " "
        self.stdscr.addstr(origin_y, self.ctx.calculate_x_origin_from_center(len(leveltxt)), leveltxt, curses.color_pair(Color.MAGENTA))

        # Print user selected
        limit_x = origin_x + self.ctx.board_width
        usertxt = " User : " + str(self.ctx.current_player) + " "
        self.stdscr.addstr(origin_y, limit_x - len(usertxt) - 1 , usertxt, curses.color_pair(Color.CYAN))

    def display_footer_game(self):
        _, origin_y = self.ctx.get_game_board_origin()
        end_y = origin_y + self.ctx.board_height

        footer_txt = "-[esc] Finish Game  -[R] Reverse Direction  -[P] Pause"
        self.stdscr.addstr(end_y + 1, self.ctx.calculate_x_origin_from_center(len(footer_txt)), footer_txt, curses.color_pair(Color.CYAN))

    def pause_game(self):
        self.stdscr.timeout(-1)
        pause_msg = " <<<<<<<< - PAUSED - >>>>>>>> "
        resume_msg = "                              "
        msg_size = len(pause_msg)
        self.stdscr.addstr(self.ctx.board_origin.y - 1, self.ctx.calculate_x_origin_from_center(msg_size), pause_msg, curses.color_pair(Color.YELLOW))

        while 1:
            pause_key = self.stdscr.getch()
            if pause_key == 112 or pause_key == 80:
                self.stdscr.addstr(self.ctx.board_origin.y - 1, self.ctx.calculate_x_origin_from_center(msg_size), resume_msg)
                self.stdscr.timeout(self.speed_level)
                break
    
    def display_game_summary(self):
        self.stdscr.clear()
        self.stdscr.nodelay(0)   
        self.stdscr.timeout(-1)
        self.ctx.draw_game_board_edge()
        text1 = "Game Over!!!!"
        text2 = "User: "+ self.ctx.current_player + "   Score: " + str(self.score_stack.get_size() + (self.current_level - 1) * MAX_SCORE_PER_LEVEL)
        text3 = "Press 'Enter' To Main Menu"
        # Display texts on screen
        center_scr_y = self.ctx.calculate_y_origin_from_center(0)
        self.stdscr.addstr(center_scr_y - 3, self.ctx.calculate_x_origin_from_center(len(text1)), text1, curses.color_pair(Color.GREEN))
        self.stdscr.addstr(center_scr_y + 1, self.ctx.calculate_x_origin_from_center(len(text2)), text2, curses.color_pair(Color.CYAN))
        self.stdscr.addstr(center_scr_y + 8, self.ctx.calculate_x_origin_from_center(len(text3)), text3, curses.color_pair(Color.RED))
        # Generate reports
        try:
            self.snake.snake_body.graph('snake_report_game_over', GameContext.REPORTS_DIRECTORY)
            self.score_stack.graph('score_report_game_over', GameContext.REPORTS_DIRECTORY)
        except Exception as e:
            print(e)

    def verify_collision_with_food(self) -> None:
        food_finded = self.items_score_list.pop_if_exist(self.snake.get_head_position())
        if food_finded is None: return False
        init_snake_size = self.snake.get_snake_size()
        self.snake.consume_item(food_finded)
        end_snake_size = self.snake.get_snake_size()
        # Update Score
        self.display_header_game()
        # Create a new food
        if init_snake_size < end_snake_size: 
            self.display_new_food()
    
    def verify_score(self):
        if self.score_stack.get_size() >= MAX_SCORE_PER_LEVEL:
            self.level_up()
            self.stdscr.clear()
            # Display messaje
            self.ctx.draw_game_board_edge()
            messaje = "Level " + str(self.current_level)
            x, y = self.ctx.calculate_origin_from_center(len(messaje), 0)
            self.stdscr.addstr(y, x, messaje)

            self.delay(1500)

            # Repaint Game
            self.stdscr.clear()
            self.ctx.draw_game_board_edge()
            self.display_header_game()
            self.display_footer_game()

            # Print snake
            self.snake.reset_snake()
            self.snake.display_body()

            # Display items on screen
            self.create_wall()
            self.display_list_score_items()

            self.delay(3000)

    def save_score(self):
        self.ctx.add_score_to_history(self.score_stack.get_size() + (self.current_level - 1) * MAX_SCORE_PER_LEVEL)
        self.ctx.add_last_score(self.snake.snake_body, self.score_stack)
    
    def game_over(self):
        self.game_status = GameStatus.GAME_OVER
        self.display_game_summary()
        self.save_score() 

    def start_snake_game(self):        
        self.stdscr.clear()
        self.stdscr.nodelay(1)
        self.stdscr.timeout(self.speed_level)

        self.ctx.draw_game_board_edge()
        self.display_header_game()
        self.display_footer_game()
        self.snake.display_body()
        self.display_new_food()

        # Begining the loop game
        while self.game_status == GameStatus.ON_GOING:
            key = self.stdscr.getch()
            # Controll of the snake's direction
            if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
                self.snake.set_direction(key)
            # Reversing the direction of the snake
            elif key == 114 or key == 82: self.snake.reverse_direction()
            # Pause game option
            elif key == 112 or key == 80: self.pause_game()   

            # Updating position and verify collision
            exist_self_collision = self.snake.make_movement()     
            # Verify score and wall collision
            self.verify_collision_with_food()
            # Verify the score to level up
            self.verify_score()
            # Game Over
            # Quit game with [esc]
            if exist_self_collision or not self.snake.is_alive() or key == 27:
                self.game_over()

        while 1:
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key == curses.KEY_ENTER or key in [10,13]: break