import curses
from Collections.graphic import IGraphable
from Game.context import GameContext
from Menu.menu_option_controller import MenuOptionController


REPORT_MENU = ["a. Snake Report", "b. Score Report", "c. Scoreboard Report", "d. Users Reports"]

class ReportOption():
    SNAKE = 0
    SCORE = 1
    SCOREBOARD = 2
    USERS = 3

class ReportMenu:
    
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
    
    def _generate_graph(self, list: IGraphable, report_name: str):
        try:
            list.graph(report_name, GameContext.REPORTS_DIRECTORY)
            self.ctx.print_message("The report was created successfully")
        except Exception as ex:
            print(str(ex))
            self.ctx.print_message("The report could not be generated")

    def _select_menu_options(self, menu_option_selected: int):
        # ************************* SNAKE REPORT *************************
        if menu_option_selected == ReportOption.SNAKE:
            snake = self.ctx.get_last_score()[0]
            self._generate_graph(snake, 'snake_report')
        # ************************* SCORE REPORT *************************
        elif menu_option_selected == ReportOption.SCORE:
            score = self.ctx.get_last_score()[1]
            self._generate_graph(score, 'score_report')
        # ************************* SCOREBOARD REPORT *************************
        elif menu_option_selected == ReportOption.SCOREBOARD:
            score_board = self.ctx.get_score_history()
            self._generate_graph(score_board, 'score_boar_report')
        # ************************* USER REPORT *************************
        elif menu_option_selected == ReportOption.USERS:
            self._generate_graph(self.ctx.user_list, 'user_report')

    def start(self):
        controll = MenuOptionController(len(REPORT_MENU) - 1)
        self.ctx.display_options_menu(REPORT_MENU, controll.get_selected_option())
        while 1:
            key = self.stdscr.getch()
            self.stdscr.clear()
            if key == curses.KEY_UP: controll.previous_option()
            elif key == curses.KEY_DOWN: controll.next_option()
            # Select option
            elif key == curses.KEY_ENTER or key in [10,13]:
                self._select_menu_options(controll.get_selected_option())
            # Exit from reports menu
            elif key == 27: break
            # Update report menu
            self.ctx.display_options_menu(REPORT_MENU, controll.get_selected_option())
            self.stdscr.refresh()