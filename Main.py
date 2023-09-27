import curses
from Menu.main_menu import MainMenu


def main(stdscr):   
    curses.curs_set(0)
    curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4,curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5,curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6,curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7,curses.COLOR_WHITE, curses.COLOR_BLACK)
    MainMenu(stdscr).start()

curses.wrapper(main)

