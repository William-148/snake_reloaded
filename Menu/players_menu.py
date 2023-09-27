import curses
from Game.context import GameContext
from Utils.colors import Color


class PlayersMenu:
    
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

    def _create_user_player(self):
        user_name = self.ctx.print_input_box("Enter user name: (Press Enter to save)")
        if len(user_name) == 0: return self.ctx.print_message("No user added")
        else:
            self.ctx.register_player(user_name)
            self.ctx.print_message("The user was saved")

    def _display_menu(self, current_player: str|None, total_users: int) -> None:
        self.stdscr.clear()
        self.ctx.draw_game_board_edge()
        text1 = "Press \"N\" to create a new user"
        text2 = "Press \"Intro\" to select user"
        text3 = "Users: " + str(total_users)
        text4 = "No Registered Users" if current_player is None else "<---          " + current_player + "          --->"
        text5 = "Press \"ESC\" to exit"
        # Drawing all text
        y = self.ctx.calculate_y_origin_from_center(0)
        self.stdscr.addstr(y - 8, self.ctx.calculate_x_origin_from_center(len(text1)), text1, curses.color_pair(Color.CYAN))
        self.stdscr.addstr(y - 7, self.ctx.calculate_x_origin_from_center(len(text2)), text2, curses.color_pair(Color.GREEN))
        self.stdscr.addstr(y - 6, self.ctx.calculate_x_origin_from_center(len(text3)), text3, curses.color_pair(Color.RED))
        self.stdscr.addstr(y, self.ctx.calculate_x_origin_from_center(len(text4)), text4, curses.color_pair(Color.GREEN))
        self.stdscr.addstr(y + 8, self.ctx.calculate_x_origin_from_center(len(text5)), text5, curses.color_pair(Color.CYAN))
        self.stdscr.refresh()
    
    def _try_to_select_player(self, player_selected: str|None) -> bool:
        """Returns boolean if a player was selected."""
        if player_selected is None:
            self.ctx.print_message("There is no user to select.")
            return False

        self.ctx.print_message("Selected User: "+ player_selected)
        self.ctx.select_player(player_selected)
        return True

    def start(self):
        iterator = self.ctx.user_list.get_iterator()
        self._display_menu(iterator.get_current_value(), self.ctx.user_list.get_size())
        while 1:
            key = self.stdscr.getch()
            # Select user
            if key == curses.KEY_ENTER or key in [10,13]:
                was_selected = self._try_to_select_player(iterator.get_current_value())
                if was_selected: break
            # Change user
            elif key == curses.KEY_LEFT: iterator.previous()
            elif key == curses.KEY_RIGHT: iterator.next()
            # Create a new player
            elif key == 110 or key == 78: 
                self._create_user_player()
                if iterator.get_current_value() is None: iterator.reset()
            # Exit Menu
            elif key == 27: break 
            # Update player menu
            self._display_menu(iterator.get_current_value(), self.ctx.user_list.get_size())
