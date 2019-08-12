import curses
import random
from curses import textpad
from Structures.DoubleLinkendList import DoubleLinkedList
from Structures.Node import DoubleNode

x_display = 80
y_display = 22
snake_body = 'O'
food_item = ('*','+')


def print_snake(stdscr,snake):
    aux = snake.head
    while aux is not None:
        coordenade = aux.data
        stdscr.addstr(coordenade[1], coordenade[0], snake_body)
        aux = aux.next_node

def create_food(snake, food,origin_x, origin_y, limit_x, limit_y):
    new_food = None    
    while new_food is None:
        coor_x = random.randint(origin_x+1, limit_x-1)
        coor_y = random.randint(origin_y+1, limit_y-1)
        type_food = random.randint(0,99)
        if type_food <=19:
            type_food = 0
        else:
            type_food = 1
        new_food = (coor_x, coor_y, type_food)
        if  snake.exist(new_food) and food.exist(new_food):
            new_food = None
        
    return new_food




def snake(stdscr):
    stdscr.clear()
    stdscr.nodelay(1)
    stdscr.timeout(150)
    h, w = stdscr.getmaxyx()

    ##Limit of the border
    origin_x = w//2 - x_display//2
    origin_y = h//2 - y_display//2
    limit_x = origin_x + x_display 
    limit_y = origin_y + y_display
    textpad.rectangle(stdscr, origin_y ,origin_x , limit_y, limit_x)##print limits

    ##Direction of the snake
    direction = curses.KEY_RIGHT

    ##Print snake
    snake = DoubleLinkedList()
    snake.addFin((origin_x+42, origin_y+11))
    snake.addFin((origin_x+41, origin_y+11))
    snake.addFin((origin_x+40, origin_y+11))
    print_snake(stdscr,snake)

    ##bocadillo
    food = DoubleLinkedList()
    food.addFin((12,8))

    ##Begining the loop game
    while 1:
        key = stdscr.getch()
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            if not ((direction == curses.KEY_RIGHT and key == curses.KEY_LEFT) or 
                (direction == curses.KEY_LEFT and key == curses.KEY_RIGHT) or 
                (direction == curses.KEY_UP and key == curses.KEY_DOWN) or
                (direction == curses.KEY_DOWN and  key == curses.KEY_UP)):
                direction = key
        
        create = random.randint(0,99)
        if create <= 20:
            new_food = create_food(snake,food, origin_x, origin_y, limit_x, limit_y)
            food.addFin(new_food)
            stdscr.addstr(new_food[1], new_food[0], food_item[new_food[2]])
            
        head = snake.head.data
        new_head = None
        if direction == curses.KEY_RIGHT:
            new_x = head[0]+1
            if new_x >= limit_x:
                new_x = origin_x+1
            new_head = (new_x, head[1])
        elif direction == curses.KEY_LEFT:
            new_x = head[0]-1
            if new_x <= origin_x:
                new_x = limit_x-1
            new_head = (new_x, head[1])
        elif direction == curses.KEY_UP:
            new_y = head[1]-1 
            if new_y <= origin_y:
                new_y = limit_y-1
            new_head = (head[0], new_y)
        elif direction == curses.KEY_DOWN:
            new_y = head[1]+1 
            if new_y >= limit_y:
                new_y = origin_y+1
            new_head = (head[0], new_y)
        
        ##Body
        if snake.exist(new_head):
            stdscr.clear()
            stdscr.nodelay(0)   
            stdscr.timeout(-1)        
            textpad.rectangle(stdscr, origin_y ,origin_x , limit_y, limit_x)
            text = "Game Over!!!!"
            stdscr.addstr(h//2 , w//2 - len(text)//2, text)
            break

        snake.addInicio(new_head)
        stdscr.addstr(new_head[1], new_head[0], snake_body)

        end = snake.end.data        
        stdscr.addstr(end[1], end[0], ' ')        
        snake.removeEnd()
        
        ##Food
        food_exist = food.exist(snake.head.data,True)
        if food_exist:
            if food_exist[2] == 0:
                #decrece
                end = snake.end.data        
                stdscr.addstr(end[1], end[0], ' ')        
                snake.removeEnd()
            else:
                #crece
                snake.addFin(end)
                stdscr.addstr(end[1], end[0], snake_body)

    stdscr.refresh()
    stdscr.getch()

#curses.wrapper(snake)
