
import curses
import Snake
from curses import textpad
from curses.textpad import Textbox, rectangle
from Structures.CircularList import CircularList 
from Structures.Queue import Queue 
from Structures.Stack import Stack 
from Structures.DoubleLinkendList import DoubleLinkedList 
from Program import FileLoad
from Program import Graphic

user_list = CircularList()
menu = ["1. Play", "2. Scoreboard", "3. User Selection", "4. Reports", "5. Bulk Loading"]
report_menu = ["a. Snake Report", "b. Score Report", "c. Scoreboard Report", "d. Users Reports"]
x_display = 80
y_display = 22
score_history = Queue()



def print_menu(stdscr, selected_row):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    x1 = w//2 - x_display//2
    y1 = h//2 - y_display//2
    textpad.rectangle(stdscr, y1 ,x1 , y1+y_display ,x1+x_display)

    max_len = 0
    for i, row in enumerate(menu):
        row_len = len(row)
        if max_len < row_len:
            max_len = row_len

    for i, row in enumerate(menu):
        x = w//2 - max_len//2
        y = h//2 - len(menu)//2 + i
        stdscr.addstr(y, x, row)

        if selected_row == i:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1)) 

    
    stdscr.refresh()

def print_reports_menu(stdscr, selected_row):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    x1 = w//2 - x_display//2
    y1 = h//2 - y_display//2
    textpad.rectangle(stdscr, y1 ,x1 , y1+y_display ,x1+x_display)

    max_len = 0
    for i, row in enumerate(report_menu):
        row_len = len(row)
        if max_len < row_len:
            max_len = row_len

    for i, row in enumerate(report_menu):
        x = w//2 - max_len//2
        y = h//2 - len(report_menu)//2 + i
        stdscr.addstr(y, x, row)

        if selected_row == i:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1)) 

    
    stdscr.refresh()

def print_user_selection(stdscr, data, user_count):
    stdscr.clear()
    h, w = stdscr.getmaxyx()  
    text = "<---          "+data+"          --->"
    text1 = "Users: "+ user_count
    text2 = "Press \"N\" to create a new user" 
    text3 = "Press \"ESC\" to exit" 
    x = w//2 - len(text)//2
    y = h//2 

    x1 = w//2 - len(text1)//2
    y1 = h//2 -7

    x2 = w//2 - len(text2)//2
    y2 = h//2 +8
    #stdscr.attron(curses.color_pair(1))

    x3 = w//2 - x_display//2
    y3 = h//2 - y_display//2
    textpad.rectangle(stdscr, y3 ,x3 , y3+y_display ,x3+x_display)
    
    stdscr.addstr(y, x, text)
    stdscr.addstr(y1, x1, text1)
    stdscr.addstr(y2, x2, text2)
    stdscr.addstr(y2+1, w//2 -len(text3)//2, text3)
    #stdscr.attroff(curses.color_pair(1)) 
    stdscr.refresh()

def print_scoreboard(stdscr,score_list):
    stdscr.clear()
    h, w = stdscr.getmaxyx()  
    text2 = "Press any key to exit"

    aux = score_list.head
    x =  w//2-24//2
    y =  h//2 - 5
    cont = 1
    stdscr.addstr(y, x , "User")
    stdscr.addstr(y, x+16, "Score")

    while aux is not None:
        user = aux.data[0]
        score = aux.data[1]
        x =  w//2-24//2
        stdscr.addstr(y+cont, x-4 , str(cont)+".")
        stdscr.addstr(y+cont, x , user)
        stdscr.addstr(y+cont, x+16, str(score)) 
        aux = aux.next_node
        cont+=1

    x2 = w//2 - len(text2)//2
    y2 = h//2 +8
    #stdscr.attron(curses.color_pair(1))

    x3 = w//2 - x_display//2
    y3 = h//2 - y_display//2
    textpad.rectangle(stdscr, y3 ,x3 , y3+y_display ,x3+x_display)
    
    stdscr.addstr(y2, x2, text2)
    #stdscr.attroff(curses.color_pair(1)) 
    stdscr.refresh()
    stdscr.getch()


def print_input_box(stdscr, message):
    stdscr.clear()
    h, w = stdscr.getmaxyx()  
    
    x = w//2 - 40//2
    y = h//2 - 1
    xt= w//2 - len(message)//2

    stdscr.addstr(y-3, xt, message)
    editwin = curses.newwin(1,40, y, x)
    ##rectangle(objeto ventana, origen esquina Y, Origen esquina X, 1+5+1, 1+30+1)
    rectangle(stdscr, y-2 ,x - 2, y + 2 , x + 40 +1 )
    stdscr.refresh()
    box = Textbox(editwin)

    # Let the user edit until Ctrl-G is struck.
    box.edit()

    # Get resulting contents
    input_text = box.gather()
    return input_text


def print_message(stdscr, message):
    stdscr.clear()
    text_skip = "Press any key to continue"
    h, w = stdscr.getmaxyx()  
    x = w//2 - len(message)//2
    y = h//2 

    x1 = w//2 - len(text_skip)//2

    x3 = w//2 - x_display//2
    y3 = h//2 - y_display//2
    textpad.rectangle(stdscr, y3 ,x3 , y3+y_display ,x3+x_display)

    stdscr.addstr(y, x, message)
    stdscr.addstr(y +6, x1, text_skip)
    stdscr.refresh()
    stdscr.getch()

def reports(stdscr, last_scores):
    selected_row = 0
    print_reports_menu(stdscr, selected_row)

    while 1:
        key = stdscr.getch()
        stdscr.clear()
        
        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1

        elif key == curses.KEY_DOWN and selected_row < len(report_menu)-1:
            selected_row += 1

        elif key == curses.KEY_ENTER or key in [10,13]:
            if selected_row == 0:
                ######## SNAKE REPORT
                if Graphic.graph(last_scores[2], "snake_report",Graphic.double_list):
                    print_message(stdscr,"The report was created successfully")
                else:
                    print_message(stdscr,"The report could not be generated")
            elif selected_row == 1:
                ######## Score Report
                if Graphic.graph(last_scores[0], "score_report",Graphic.stack_list):
                    print_message(stdscr,"The report was created successfully")
                else:
                    print_message(stdscr,"The report could not be generated")
            elif selected_row == 2:
                ######## ScoreBoard Report
                if Graphic.graph(score_history, "score_boar_report",Graphic.queue_list):
                    print_message(stdscr,"The report was created successfully")
                else:
                    print_message(stdscr,"The report could not be generated")
            elif selected_row == 3:
                ######## User Report
                ### Generar reporte de lista circular doble
                if Graphic.graph(user_list, "user_report",Graphic.circular_list):
                    print_message(stdscr,"The report was created successfully")
                else:
                    print_message(stdscr,"The report could not be generated")


        elif key == 27:
            break

        print_reports_menu(stdscr, selected_row)
        stdscr.refresh()

def main(stdscr):   

    curses.curs_set(0)
    curses.init_pair(1,curses.COLOR_CYAN, curses.COLOR_WHITE)
    selected_row = 0 
    user_list.addEnd("usuario")
    user_game = None
    last_score = (Stack(), 0, DoubleLinkedList())

    print_menu(stdscr, selected_row)

    while 1:
        ######################## MENU START ######################
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1

        elif key == curses.KEY_DOWN and selected_row < len(menu)-1:
            selected_row += 1

        elif key == curses.KEY_ENTER or key in [10,13]:
            if selected_row == 0:
                ############## OPTION 1 - PLAY GAME  ###############
                if user_game is not None:
                    last_score = Snake.snake(stdscr, user_game)
                    score_history.enqueue((user_game, last_score[0].size + (last_score[1]-1)*Snake.max_score))
                    if score_history.size > 10:
                        score_history.dequeue()
                else:
                    user_name = print_input_box(stdscr, "No user selected. Enter user name: (Press Enter to play)")  
                    if len(user_name)  ==0:
                        print_message(stdscr,"No user added")
                    else:
                        user_game = user_name
                        user_list.addEnd(user_name)                        
                        last_score = Snake.snake(stdscr, user_game)
                        score_history.enqueue((user_game, last_score[0].size + (last_score[1]-1)*Snake.max_score))
                        if score_history.size > 10:
                            score_history.dequeue()

            elif selected_row == 1:
                ############## OPTION 2 - SCORE BOARD ###############
                print_scoreboard(stdscr, score_history)

            elif selected_row == 2:
                ############## OPTION 3 USER SELECT   ###############
                
                list_data = user_list.getList()
                print_user_selection(stdscr,list_data.data, str(user_list.size))
                
                while 1:
                    key = stdscr.getch()
                    if key == curses.KEY_ENTER or key in [10,13]:                        
                        print_message(stdscr,"Selected User: "+ list_data.data)
                        user_game = list_data.data
                        break
                        
                    elif key == curses.KEY_LEFT:
                        list_data = list_data.previous_node
                        
                    elif key == curses.KEY_RIGHT:
                        list_data = list_data.next_node
                        
                    elif key == 110 or key == 78:
                        user_name = print_input_box(stdscr, "Enter user name: (Press Enter to save)")  
                        if len(user_name)  ==0:
                            print_message(stdscr,"No user added")
                        else:
                            user_list.addEnd(user_name)
                            print_message(stdscr,"The user was saved")
                    elif key == 27:    
                        break
                    
                    print_user_selection(stdscr,list_data.data,str(user_list.size))
                
            elif selected_row == 3:
                ############## OPTION 4 - REPORTS   ###############
                reports(stdscr, last_score)

            elif selected_row == 4:
                ############## OPTION 5 - BULK LOADING   ###############
                file_name = print_input_box(stdscr, "Enter file name: (Enter to continue)")
                file_name += ".csv"
                file_name = FileLoad.delete_space(file_name)
                actual_user = user_list.size

                success = FileLoad.read(file_name, user_list)
                if actual_user == user_list.size:
                    if success == 0:
                        print_message(stdscr,"File not found")
                    else:
                        print_message(stdscr,"No data added")
                else:
                    print_message(stdscr,"The file was loaded")
                
                
            
        print_menu(stdscr, selected_row)
        stdscr.refresh()



curses.wrapper(main)

