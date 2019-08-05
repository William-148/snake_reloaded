
import curses
from curses import textpad
from curses.textpad import Textbox, rectangle
from Structures.CircularList import CircularList 
from Program import FileLoad

user_list = CircularList()

menu = ["1. Play", "2. Scoreboard", "3. User Selection", "4. Reports", "5. Bulk Loading"]
x_display = 80
y_display = 22
user_game = "usuario" 

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

def print_user_selection(stdscr, data, user_count):
    stdscr.clear()
    h, w = stdscr.getmaxyx()  
    text = "<---          "+data+"          --->"
    text1 = "Users: "+ user_count
    text2 = "Press \"N\" to create a new user" 
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
    #stdscr.attroff(curses.color_pair(1)) 
    stdscr.refresh()

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

    
def main(stdscr):   

    curses.curs_set(0)
    curses.init_pair(1,curses.COLOR_CYAN, curses.COLOR_WHITE)
    selected_row = 0 
    user_list.addEnd("usuario")
    

    print_menu(stdscr, selected_row)

    while 1:
        
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1

        elif key == curses.KEY_DOWN and selected_row < len(menu)-1:
            selected_row += 1

        elif key == curses.KEY_ENTER or key in [10,13]:
            if selected_row == 0:
                stdscr.addstr(0,0, "eligió opcion 1")
            elif selected_row == 1:
                stdscr.addstr(0,0, "eligió opcion 2")
            elif selected_row == 2:
                
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
                        
                    
                    print_user_selection(stdscr,list_data.data,str(user_list.size))
                    
                    

                

            elif selected_row == 3:
                stdscr.addstr(0,0, "eligió opcion 4")
            elif selected_row == 4:
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
                
                
            #stdscr.refresh()
            #stdscr.getch()
        print_menu(stdscr, selected_row)
        stdscr.refresh()



curses.wrapper(main)

