import curses
from curses import textpad
from Collections.circular_list import CircularList
from Collections.doubly_linked_list import DoublyLinkedList
from Collections.iterator import Iterator
from Collections.queue import Queue
from Collections.stack import Stack
from Utils.colors import Color
from Utils.coordinate import Coordinate
from Utils.data_persistence import read_local_score_history, read_local_user_data, write_local_score_history_queue, write_local_score_to_history, write_local_user


class GameContext:
    REPORTS_DIRECTORY = 'Reports'
    MAX_SIZE_SCORE_HISTORY = 10

    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr
        self.board_width = 80
        self.board_height = 22
        self.current_player = None
        self.user_list = CircularList()
        self.score_history = Queue()
        self.set_limits_board()
        self.load_users_from_file()
        self.load_score_history_from_file()
        self.last_score = (DoublyLinkedList(), Stack())
        """Tuple: Index 0 is a 'DoublyLinkedList' class instance. Index 1 is 'Stack' class instance."""

    def load_users_from_file(self):
        read_local_user_data(lambda user: self.user_list.add_end(user))

    def load_score_history_from_file(self):
        read_local_score_history(lambda user, score: self.score_history.enqueue((user, score)))
        
    def set_limits_board(self):
        origin_x, origin_y = self.calculate_origin_from_center(self.board_width, self.board_height)
        self.board_origin = Coordinate(origin_x, origin_y)
        """Board origin coordinate (instance of class 'Coordinate')"""
        self.board_end = Coordinate(origin_x + self.board_width, origin_y + self.board_height)
        """Board end coordinate (instance of class 'Coordinate')"""

    def add_score_to_history(self, total_score: int) -> None:
        if not self.is_player_selected(): return
        user_score = (self.current_player, total_score)
        self.score_history.enqueue(user_score)
        if self.score_history.get_size() > GameContext.MAX_SIZE_SCORE_HISTORY:
            self.score_history.dequeue()
            write_local_score_history_queue(self.score_history)
        else:
            write_local_score_to_history(user_score)

    def get_score_history(self): return self.score_history

    def add_last_score(self, snake_body: DoublyLinkedList, score: Stack) -> None:
        self.last_score = (snake_body, score)

    def get_last_score(self): return self.last_score

    def select_player(self, user_name: str) -> None:
        """Select a player for the next game."""
        self.current_player = user_name

    def register_player(self, user_name: str) -> None:
        """Registers a player locally and adds him to the player list."""
        self.user_list.add_end(user_name)
        write_local_user(user_name)
    
    def is_player_selected(self) -> bool:
        """Determine if a player has been selected for the next game."""
        return self.current_player is not None
    
    def calculate_origin_from_center(self, element_width, element_height) -> tuple[int, int]:
        """
        Calculates the origin coordinate of an element to be able to draw it in the center of the screen.
        Returns:
            (number, number): Tuple containing the coordinate in x and y.
        """
        # Getting max-heigth and max-width of console screen
        max_height, max_width = self.stdscr.getmaxyx() 
        return (
            max_width // 2 - element_width// 2 ,
            max_height // 2 - element_height // 2
        )
    
    def calculate_x_origin_from_center(self, element_width) -> int:
        """Calculates the X origin coordinate of an element to be able to draw it in the center of the screen."""
        # Getting max-heigth and max-width of console screen
        _, max_width = self.stdscr.getmaxyx() 
        return max_width // 2 - element_width// 2
    
    def calculate_y_origin_from_center(self, element_height) -> int:
        """Calculates the Y origin coordinate of an element to be able to draw it in the center of the screen."""
        max_height, _ = self.stdscr.getmaxyx() 
        return max_height // 2 - element_height // 2
    
    def get_game_board_origin(self) -> tuple[int, int]:
        return self.calculate_origin_from_center(self.board_width, self.board_height)
    
    def get_game_board_end(self) -> tuple[int, int]:
        x, y = self.calculate_origin_from_center(self.board_width, self.board_height)
        return (x + self.board_width, y + self.board_height)
    
    def draw_game_board_edge(self):
        x, y = self.get_game_board_origin()
        # Drawing rectangle specifiying the origin and end
        self.stdscr.attron(curses.color_pair(Color.RED))
        textpad.rectangle(self.stdscr, y ,x , y + self.board_height, x + self.board_width)
        self.stdscr.attroff(curses.color_pair(Color.RED)) 
    
    def draw_exit_with_any_key(self):
        """Draw the text 'Press any key to exit' at the bottom of the screen."""
        text = "Press any key to exit"
        # Getting origin for text
        x, y = self.calculate_origin_from_center(len(text), 0)
        # Drawing text
        self.stdscr.addstr(y + self.board_height//2 - 2, x, text, curses.color_pair(Color.CYAN))

    def print_message(self, message):
        self.stdscr.clear()
        self.draw_game_board_edge()
        self.draw_exit_with_any_key()
        # Getting origin coordinate for message
        x, y = self.calculate_origin_from_center(len(message), 0)
        # Draw message on screen
        self.stdscr.addstr(y, x, message)
        # Refresh and wait until a key is pressed
        self.stdscr.refresh()
        self.stdscr.getch()

    def print_input_box(self, message) -> str:
        """Display a textbox on the screen and returns the input result (string)."""
        self.stdscr.clear()
        self.draw_game_board_edge()
        # Drawing message
        msg_x_origin, msg_y_origin = self.calculate_origin_from_center(len(message), 0)
        self.stdscr.addstr(msg_y_origin - 4, msg_x_origin, message)

        # Drawing new window
        window_width = 40
        window_x_origin, window_y_origin = self.calculate_origin_from_center(window_width, 0)
        window_y_origin = window_y_origin - 1
        editwin = curses.newwin(1, window_width, window_y_origin, window_x_origin)
        box = textpad.Textbox(editwin)

        # Drawing rectangle
        # rectangle(objeto ventana, origen esquina Y, Origen esquina X, 1+5+1, 1+30+1)
        textpad.rectangle(self.stdscr, window_y_origin - 2, window_x_origin - 2, window_y_origin + 2 , window_x_origin + window_width + 1)
        self.stdscr.refresh()

        # Let the user edit until Ctrl-G is struck.
        box.edit()

        # Get resulting contents
        input_text = box.gather()
        return input_text
        
    def print_scoreboard(self):
        self.stdscr.clear()
        self.draw_game_board_edge()
        self.draw_exit_with_any_key()

        # Calculate user's score table origin
        x, y = self.calculate_origin_from_center(24, 0)
        y = y - 5

        # Drawing table header
        self.stdscr.addstr(y, x , "User", curses.color_pair(Color.CYAN))
        self.stdscr.addstr(y, x + 16, "Score", curses.color_pair(Color.CYAN))

        # Drawing table rows (users score)
        iterator = Iterator(self.score_history)
        cont = 1
        while iterator.has_current():
            data = iterator.get_current_value()
            user = data[0]
            score = data[1]
            self.stdscr.addstr(y + cont, x - 4, str(cont) + ".")
            self.stdscr.addstr(y + cont, x, user)
            self.stdscr.addstr(y + cont, x + 16, str(score)) 
            iterator.next()
            cont += 1

        self.stdscr.refresh()
        self.stdscr.getch()

    def display_options_menu(self, option_list: list[str], menu_option_selected: int):
        self.stdscr.clear()
        self.draw_game_board_edge()

        # Determining wich menu option has maximum length
        max_length_option = 0
        for i, row in enumerate(option_list):
            row_len = len(row)
            if max_length_option < row_len:
                max_length_option = row_len

        # Drawing each menu options
        x, y = self.calculate_origin_from_center(max_length_option, len(option_list))
        for i, row in enumerate(option_list):
            y_option_coordinate = y + i
            self.stdscr.addstr(y_option_coordinate, x, row)
            # Applying color to selected option
            if menu_option_selected == i:
                self.stdscr.addstr(y_option_coordinate, x, row, curses.color_pair(Color.CYAN))

        self.stdscr.refresh()