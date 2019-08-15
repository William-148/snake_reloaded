import curses
import random
from Program import Graphic
from curses import textpad
from Structures.DoubleLinkendList import DoubleLinkedList
from Structures.Stack import Stack

x_display = 80
y_display = 22
max_score = 15
speed_init = 160
speed_plus = 10
snake_body = '©'
food_item = ('*','+', '█')


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

def create_wall(snake, food, origin_x, origin_y, limit_x, limit_y):
    new_wall = None    
    while new_wall is None:
        coor_x = random.randint(origin_x+1, limit_x-1)
        coor_y = random.randint(origin_y+1, limit_y-1)
        
        new_wall = (coor_x, coor_y, 2)
        if  snake.exist(new_wall) and food.exist(new_wall):
            new_wall = None
        
    return new_wall




def snake(stdscr, user):
    speed_level = speed_init
    stdscr.clear()
    stdscr.nodelay(1)
    stdscr.timeout(speed_level)
    h, w = stdscr.getmaxyx()
    
    ##Print limit of the border
    origin_x = w//2 - x_display//2
    origin_y = h//2 - y_display//2
    limit_x = origin_x + x_display 
    limit_y = origin_y + y_display
    textpad.rectangle(stdscr, origin_y ,origin_x , limit_y, limit_x)##print limits

    ##Print score
    score = Stack()
    scoretxt = " Score : "+str(score.size)+" "
    stdscr.addstr(origin_y, origin_x +2 , scoretxt )

    ##Print Level
    level = 1
    leveltxt = " SNAKE RELOADED | LEVEL : 1 "
    stdscr.addstr(origin_y, w//2 - len(leveltxt)//2 , leveltxt )

    ##Print user selected
    usertxt = " User : "+user+" "
    stdscr.addstr(origin_y, limit_x -len(usertxt) -1 , usertxt)


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
    ##Print bocadillo
    new_food = create_food(snake,food, origin_x, origin_y, limit_x, limit_y)
    food.addFin(new_food)
    stdscr.addstr(new_food[1], new_food[0], food_item[new_food[2]])

    ##Begining the loop game
    while 1:
        key = stdscr.getch()
        ##Controll of the snake's direction
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            if not ((direction == curses.KEY_RIGHT and key == curses.KEY_LEFT) or 
                (direction == curses.KEY_LEFT and key == curses.KEY_RIGHT) or 
                (direction == curses.KEY_UP and key == curses.KEY_DOWN) or
                (direction == curses.KEY_DOWN and  key == curses.KEY_UP)):
                direction = key     
        ##Reverse snake        
        elif key == 114 or key == 82:
            snake.reverse()
            head = snake.head.data
            neck = snake.head.next_node.data
            if head[1] == neck[1]:
                if head[0] > neck[0]:
                    direction = curses.KEY_RIGHT
                else:
                    direction = curses.KEY_LEFT
            elif head[0] == neck[0]:
                if head[1] > neck[1]:
                    direction = curses.KEY_DOWN
                else:
                    direction = curses.KEY_UP
        ##Pause
        elif key == 112 or key == 80:
            stdscr.timeout(-1)
            
            pausetext = " <<<<<<<< - PAUSED - >>>>>>>> "
            resumetext= "                              "
            txtsize = len(pausetext)
            stdscr.addstr(origin_y - 1, w//2 - txtsize//2 , pausetext )
            Graphic.graph(snake, "snake_report_pause",Graphic.double_list)
            Graphic.graph(score, "score_report_pause",Graphic.stack_list)           

            while 1:
                pause_key = stdscr.getch()

                if pause_key == 112 or key == 80:
                    stdscr.addstr(origin_y - 1, w//2 - txtsize//2 , resumetext )
                    stdscr.timeout(speed_level)
                    break     

        ##Control of snake movement    
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
        
        
        ##Check if the route is in the snake's body, if is true, is game over
        if snake.exist(new_head):
            stdscr.clear()
            stdscr.nodelay(0)   
            stdscr.timeout(-1)        
            textpad.rectangle(stdscr, origin_y ,origin_x , limit_y, limit_x)
            text = "Game Over!!!!"
            text0 = "User: "+ user +"   Score: "+str(score.size + (level-1)*max_score)
            text1 = "Press 'Enter' To Main Menu"
            stdscr.addstr(h//2 , w//2 - len(text)//2, text)
            stdscr.addstr(h//2 + 2 , w//2 - len(text0)//2, text0)
            stdscr.addstr(limit_y -3 , w//2 - len(text1)//2, text1)
            Graphic.graph(snake, "snake_report_gameover",Graphic.double_list)
            Graphic.graph(score, "score_report_gameover",Graphic.stack_list)  
            break

        ##Add the new snake's head to the list and print it    
        snake.addInicio(new_head)
        stdscr.addstr(new_head[1], new_head[0], snake_body)
        
        ##Remove in the list the snake's end 
        end = snake.end.data        
        stdscr.addstr(end[1], end[0], ' ')        
        snake.removeEnd()
        
        
        ##Food     
        food_exist = food.exist(snake.head.data,True)
        if food_exist:            
            if food_exist[2] == 0:
                #decrece
                if snake.size > 3:
                    end = snake.end.data        
                    stdscr.addstr(end[1], end[0], ' ')        
                    snake.removeEnd()
                score.pop()
                
            elif food_exist[2] == 1:
                #crece
                snake.addFin(end)
                stdscr.addstr(end[1], end[0], snake_body)
                score.push(food_exist)
            else:
                stdscr.clear()
                stdscr.nodelay(0)   
                stdscr.timeout(-1)        
                textpad.rectangle(stdscr, origin_y ,origin_x , limit_y, limit_x)
                text = "Game Over!!!!"
                text0 = "User: "+ user +"   Score: "+str(score.size + (level-1)*max_score)
                text1 = "Press 'Enter' To Main Menu"
                stdscr.addstr(h//2 , w//2 - len(text)//2, text)
                stdscr.addstr(h//2 + 2 , w//2 - len(text0)//2, text0)
                stdscr.addstr(limit_y -3 , w//2 - len(text1)//2, text1)
                Graphic.graph(snake, "snake_report_gameover",Graphic.double_list)
                Graphic.graph(score, "score_report_gameover",Graphic.stack_list)  
                break
            
            ##Update Score
            scoretxt = " Score : "+str(score.size)+" "
            stdscr.addstr(origin_y, origin_x +2 , scoretxt )
            ##Create a new bocadillo
            new_food = create_food(snake,food, origin_x, origin_y, limit_x, limit_y)
            food.addFin(new_food)
            stdscr.addstr(new_food[1], new_food[0], food_item[new_food[2]])
        
        ##Check the score
        if score.size == max_score:
            level +=1
            stdscr.clear()
            ##Messaje
            textpad.rectangle(stdscr, origin_y ,origin_x , limit_y, limit_x)##print limits
            messaje = "Level "+str(level)
            stdscr.addstr(h//2, w//2 - len(messaje)//2 , messaje )
            stdscr.timeout(1500)
            stdscr.getch()
            speed_level -= speed_plus
            stdscr.timeout(speed_level )
            stdscr.clear()
            ##Repaint borders
            textpad.rectangle(stdscr, origin_y ,origin_x , limit_y, limit_x)##print limits
            stdscr.addstr(origin_y, limit_x -len(usertxt) -1 , usertxt)
            ##Update new level score
            score.clean()
            stdscr.addstr(origin_y, origin_x +2 , " Score: 0 ")
            leveltxt = " SNAKE RELOADED | LEVEL : "+ str(level)+" "
            stdscr.addstr(origin_y, w//2 - len(leveltxt)//2 , leveltxt )
            ##Direction of the snake
            direction = curses.KEY_RIGHT
            ##Add walls
            
            new_wall = create_wall(snake,food, origin_x, origin_y, limit_x, limit_y)
            food.addFin(new_wall)

            ##Print snake
            snake.clean()
            snake.addFin((origin_x+42, origin_y+11))
            snake.addFin((origin_x+41, origin_y+11))
            snake.addFin((origin_x+40, origin_y+11))
            print_snake(stdscr,snake)
            ##Repaint Food
            update_food = food.head
            while update_food is not None:
                stdscr.addstr(update_food.data[1], update_food.data[0], food_item[update_food.data[2]])
                update_food = update_food.next_node

    while 1:
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_ENTER or key in [10,13]:
            break
    return (score, level, snake)

#curses.wrapper(snake)
