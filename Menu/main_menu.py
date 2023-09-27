import curses
from Game.context import GameContext
from Game.manager import GameManager
from Menu.menu_option_controller import MenuOptionController
from Menu.players_menu import PlayersMenu
from Menu.report_menu import ReportMenu


MAIN_MENU = ["1. Play", "2. Scoreboard", "3. User Selection", "4. Reports", "5. Exit"]

class MenuOption():
    PLAY = 0
    SCOREBOARD = 1
    USER_SELECTION = 2
    REPORTS = 3
    EXIT = 4

class MainMenu:
    
    def __init__(self, stdscr) -> None:
        """
        Parameters:
            stdscr (instance of curses.window class from curses library): 
                An object that provides methods and attributes to perform writing and reading operations 
                on the screen, such as printing text, moving the cursor, and responding to keyboard events.
        """
        self.stdscr = stdscr
        self.ctx = GameContext(stdscr) 

    def select_main_menu_options(self, menu_option_selected):
        # ************************* OPTION 1 - PLAY GAME *************************
        if menu_option_selected == MenuOption.PLAY:
            # Validating if a player is selected.
            if self.ctx.validate_selected_user():
                GameManager(self.stdscr, self.ctx).start_snake_game()
        # ************************* OPTION 2 - SCORE BOARD *************************
        elif menu_option_selected == MenuOption.SCOREBOARD:
            self.ctx.print_scoreboard()
        #************************* OPTION 3 USER SELECTION *************************
        elif menu_option_selected == MenuOption.USER_SELECTION:
            PlayersMenu(self.stdscr, self.ctx).start()
        # ************************* OPTION 4 - REPORTS *************************
        elif menu_option_selected == MenuOption.REPORTS:
            ReportMenu(self.stdscr, self.ctx).start()

    def start(self):
        controll = MenuOptionController(len(MAIN_MENU) - 1)
        self.ctx.display_options_menu(MAIN_MENU, controll.get_selected_option())
        while 1:
            # ********************** MENU START **********************
            key = self.stdscr.getch()
            self.stdscr.clear()
            if key == curses.KEY_UP: controll.previous_option()
            elif key == curses.KEY_DOWN: controll.next_option()
            # Select option
            elif key == curses.KEY_ENTER or key in [10,13]:
                self.select_main_menu_options(controll.get_selected_option())
                if controll.get_selected_option() == MenuOption.EXIT: break
            # Updating main menu
            self.ctx.display_options_menu(MAIN_MENU, controll.get_selected_option())
