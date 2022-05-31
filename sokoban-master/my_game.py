#!../bin/python

from logging import raiseExceptions
import sys
import pygame
import string
import queue
import random
import time
from agent import Agent
class game:

    def is_valid_value(self,char):
        if ( char == ' ' or #floor
            char == '#' or #wall
            char == '@' or #agent on floor
            char == '=' or #agent1 on floor

            char == '.' or #dock
            char == '*' or #box on dock
            char == '$' or #box
            char == '%' or #dividing wall
            
            char == '1' or #num1
            char == '2' or #num2
            char == '3' or #num3
            char == '4' or #num4
            char == '5' or #num5

            char == 'a' or #dock_num1
            char == 'b' or #dock_num2
            char == 'c' or #dock_num3
            char == 'd' or #dock_num4
            char == 'e' or #dock_num5
            char == 'z' or
            char == '+' ): #agent on dock
            return True
        else:
            return False

    def __init__(self,filename,level):
        self.queue = queue.LifoQueue()
        self.matrix = []
#        if level < 1 or level > 50:
        if int(level) < 1:
            print("ERROR: Level "+str(level)+" is out of range")
            sys.exit(1)
        else:
            file = open(filename,'r')
            level_found = False
            for line in file:
                row = []
                if not level_found:
                    if  "Level "+str(level) == line.strip():
                        level_found = True
                else:
                    if line.strip() != "":
                        row = []
                        for c in line:
                            if c != '\n' and self.is_valid_value(c):
                                row.append(c)
                            elif c == '\n': #jump to next row when newline
                                continue
                            else:
                                print("ERROR: Level "+str(level)+" has invalid value "+c)
                                sys.exit(1)
                        self.matrix.append(row)
                    else:
                        break



    def load_size(self):
        x = 0
        y = len(self.matrix)
        for row in self.matrix:
            print(row)
            if len(row) > x:
                x = len(row)
        return (x * 32, y * 32)

    def get_matrix(self):
        return self.matrix

    def print_matrix(self):
        for row in self.matrix:
            for char in row:
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write('\n')

    def get_content(self,x,y):
        return self.matrix[y][x]

    def set_content(self,x,y,content):
        if self.is_valid_value(content):
            self.matrix[y][x] = content
        else:
            print("ERROR: Value '"+content+"' to be added is not valid")

    def agent_position(self, agent):
        
        x = 0
        y = 0
        if agent.id ==1:
            for row in self.matrix:
                for i in range(6):
                    if row[i] == '@' or row[i] == '+':
                        return (x, y, row[i])
                    else:
                        x = x + 1
                y = y + 1
                x = 0


        elif agent.id ==2:
            for row in self.matrix:
                for i in range(6):
                    if row[i+5] == '=' or row[i+5] == '+':
                        return (x, y, row[i+5])
                    else:
                        x = x + 1
                y = y + 1
                x = 5

        else: 
            raiseExceptions
            print("Invalid Id")

        '''
        for row in self.matrix:
            print(len(row))
            #taalla virhus
            for pos in row:
                if agent.id ==1:
                    print(pos)
                    if pos == '@' or pos == '+':
                        return (x, y, pos)
                    else:
                        x = x + 1
                elif agent.id ==2 :
                    if pos == '=' or pos == '+':
                        return (x, y, pos)
                    else:
                        x = x + 1
                else:
                    raiseExceptions
                    print("Invalid Id")
            y = y + 1
            x = 0
            '''

    def can_move(self,x,y, agent):
        agent = agent
        return self.get_content(agent[0]+x,agent[1]+y) not in ['%','#','*','$','1','2','3','4','5']

    def next(self,x,y, agent ):
        agent = agent
        return self.get_content(agent[0]+x,agent[1]+y)
    """
    def open_obstacle_agent(self,x,y, agent):
        return (self.next(x,y,agent) in ['.'])
    """
    def can_push(self,x,y,agent):
        options = ['1','2','3','4','5','a','b','c','d','e']
        boxes_in_dock = ['a','b','c','d','e', ' ']
        return (self.next(x,y,agent) in options and self.next(x+x,y+y,agent) in boxes_in_dock)

    def is_completed(self):
        for row in self.matrix:
            for cell in row:
                if cell == 'z':
                    return False
        return True

    def move_box(self,x,y,a,b):
#        (x,y) -> move to do
#        (a,b) -> box to move
        current_box = self.get_content(x,y)
        future_box = self.get_content(x+a,y+b)
        boxes = ['1','2','3','4','5']
        boxes_in_dock = ['a','b','c','d','e']

        if current_box in boxes and future_box == ' ':
            self.set_content(x+a,y+b,current_box)
            self.set_content(x,y,' ')
        elif current_box in boxes and future_box in boxes_in_dock[boxes.index(current_box)]:
            self.set_content(x+a,y+b,'*')
            self.set_content(x,y,' ')
        elif current_box == '*' and future_box == ' ':
            self.set_content(x+a,y+b,current_box)
            self.set_content(x,y,boxes_in_dock[boxes.index(current_box)])
        elif current_box == '*' and future_box in boxes_in_dock[boxes.index(current_box)]:
            self.set_content(x+a,y+b,'*')
            self.set_content(x,y,boxes_in_dock[boxes.index(current_box)])




    def move(self,x,y,save, agent):
        print()
        print(" X",x," Y",y)


        agent_position = self.agent_position(agent)
        print(agent_position )
        if self.can_move(x,y, agent_position):
            current = agent_position
            #print("get content ",self.get_content(agent[0]+x,agent[1]+y) )
            future = self.next(x,y,agent_position)

            print("Agent ID :", agent.id, "FUTURE ", future)

            #print("current: ",current[0], " current[1]: ", current[1] )
            #print("current[0]+x: ",current[0]+x, " current[1]+y: ", current[1]+y)
            boxes = ['1','2','3','4','5']
            boxes_in_dock = ['a','b','c','d','e','.']

            if (current[2] == '@' or current[2] == '=') and future == ' ':
                self.set_content(current[0]+x,current[1]+y,current[2])
                self.set_content(current[0],current[1],' ')
                if save: self.queue.put((x,y,False))
            
            

            elif (current[2] == '@' or current[2] == '=') and future == '.':
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],' ')
            
                #OBSTACLE 1
                for x in range(10): #put 10
                    if(self.get_content(x,current[1]+y-1) == '$'):
                        self.set_content(x,current[1]+y-1,' ')


            
            elif current[2] == '+' and future == ' ':
                
                if agent.id == 1:
                    self.set_content(current[0]+x,current[1]+y,'@')
                elif agent.id == 2:
                    self.set_content(current[0]+x,current[1]+y,'=')

                self.set_content(current[0],current[1],'.')
        
                #if save: self.queue.put((x,y,False))



            elif current[2] == '+' and future == 'a':
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],'a')
                #if save: self.queue.put((x,y,False))
            elif current[2] == '+' and future == 'b':
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],'b')
            elif current[2] == '+' and future == 'c':
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],'c')
                #if save: self.queue.put((x,y,False))
            elif current[2] == '+' and future == 'd':
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],'d')
            elif current[2] == '+' and future == 'e':
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],'e')
            elif current[2] == '+' and future == '.':
                print("virhe")
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],'.')
            
            #finish line
            elif (current[2] == '@' or current[2] == '=')  and future == 'z':
                self.set_content(current[0]+x,current[1]+y,current[2])
                self.set_content(current[0],current[1],' ')
                       



        elif self.can_push(x,y,agent_position):
            current = agent_position
            future = self.next(x,y,agent_position)
            future_box = self.next(x+x,y+y,agent_position)
            boxes = ['1','2','3','4','5']
            boxes_in_dock = ['a','b','c','d','e']
            if (current[2] == '@'  or current[2] == '=') and future in boxes and future_box == ' ':
                print("F1 box ", future)
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,current[2])
                #if save: self.queue.put((x,y,True))
            elif (current[2] == '@' or current[2] == '=') and future in boxes and future_box in boxes_in_dock[boxes.index(future)]:
                print("F1 box ", future)
                print("Future__: ", boxes_in_dock[boxes.index(future)])

                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,current[2])
                if save: self.queue.put((x,y,True))
            elif (current[2] == '@' or current[2] == '=') and future == '*' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'+')
                if save: self.queue.put((x,y,True))
            elif (current[2] == '@' or current[2] == '=') and future == '*' and future_box in boxes_in_dock[boxes.index(future)]:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'+')
                if save: self.queue.put((x,y,True))
            if current[2] == '+' and future in boxes and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],boxes_in_dock[boxes.index(future)])
                self.set_content(current[0]+x,current[1]+y,current[2])
                if save: self.queue.put((x,y,True))
            elif current[2] == '+' and future in boxes and future_box in boxes_in_dock[boxes.index(future)]:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],boxes_in_dock[boxes.index(future)])
                self.set_content(current[0]+x,current[1]+y,'+')
                if save: self.queue.put((x,y,True))
            elif current[2] == '+' and future == '*' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],boxes_in_dock[boxes.index(future)])
                self.set_content(current[0]+x,current[1]+y,'+')
                if save: self.queue.put((x,y,True))
            elif current[2] == '+' and future == '*' and future_box in boxes_in_dock[boxes.index(future)]:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],boxes_in_dock[boxes.index(future)])
                self.set_content(current[0]+x,current[1]+y,'+')
                if save: self.queue.put((x,y,True))


        agent_position = None    
"""
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
"""    
def print_game(matrix,screen):
    """
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    """
    screen.fill(background)
    x = 0
    y = 0
    for row in matrix:
        for char in row:
            if char == '%': #dividing_wall
                screen.blit(dividing_wall,(x,y)) 
            if char == '=': #agent1
                screen.blit(agent1,(x,y)) 
            if char == ' ': #floor
                screen.blit(floor,(x,y))
            elif char == '#': #wall
                screen.blit(wall,(x,y))
            elif char == '@': #agent on floor
                screen.blit(agent,(x,y))
            elif char == '.': #dock
                screen.blit(docker,(x,y))
            elif char == '*': #box on dock
                screen.blit(box_docked,(x,y))
            elif char == '$': #box
                screen.blit(box,(x,y))
            elif char == '+': #agent on dock
                screen.blit(agent_docked,(x,y))

            elif char == '1': #num1
                screen.blit(num1,(x,y))
            elif char == '2': #num2
                screen.blit(num2,(x,y))
            elif char == '3': #num3
                screen.blit(num3,(x,y))
            elif char == '4': #num4
                screen.blit(num4,(x,y))
            elif char == '5': #num5
                screen.blit(num5,(x,y))

            elif char == 'a': #dock_num1
                screen.blit(dock_num1,(x,y))
            elif char == 'b': #dock_num2
                screen.blit(dock_num2,(x,y))
            elif char == 'c': #dock_num3
                screen.blit(dock_num3,(x,y))
            elif char == 'd': #dock_num4
                screen.blit(dock_num4,(x,y))
            elif char == 'e': #dock_num5
                screen.blit(dock_num5,(x,y))

            elif char == 'z': #dock_num5
                screen.blit(finish,(x,y))

            x = x + 32
        x = 0
        y = y + 32


def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == pygame.KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def display_end(screen):
    message = "Level Completed"
    fontobject = pygame.font.Font(None,18)
    pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
    pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
    pygame.display.flip()




def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + "".join(current_string)
)
  while 1:
    inkey = get_key()
    if inkey == pygame.K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == pygame.K_RETURN:
      break
    elif inkey == pygame.K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + "".join(current_string)
)
  return "".join(current_string)


def start_game():
    start = pygame.display.set_mode((320,240))

    #game_option = ask(pygame.display.set_mode((320,1500)),"Game option: \nX: one agent\n Y: agent1 vs agent2\n Z: user vs agent2")

    level = ask(start,"Select Level")
    if int(level) > 0: # and (game_option=='X' or game_option=='Y' or game_option=='Z'):
        return level #, game_option
    else:
        print("ERROR: Invalid Level or game option: "+str(level))
        sys.exit(2)




    
dividing_wall = pygame.image.load('images/wall1.png')
agent1 = pygame.image.load('images/agent1.png')

wall = pygame.image.load('images/wall.png')
floor = pygame.image.load('images/floor.png')
box = pygame.image.load('images/bomx.png')
box_docked = pygame.image.load('images/box_docked.png')
agent = pygame.image.load('images/agent.png')
agent_docked = pygame.image.load('images/agent_dock.png')
docker = pygame.image.load('images/dock.png')

num1 = pygame.image.load('images/n1.png')
num2 = pygame.image.load('images/n2.png')
num3 = pygame.image.load('images/n3.png')
num4 = pygame.image.load('images/n4.png')
num5 = pygame.image.load('images/n5.png')

dock_num1 = pygame.image.load('images/dock_n1.png')
dock_num2 = pygame.image.load('images/dock_n2.png')
dock_num3 = pygame.image.load('images/dock_n3.png')
dock_num4 = pygame.image.load('images/dock_n4.png')
dock_num5 = pygame.image.load('images/dock_n5.png')
finish = pygame.image.load('images/finish.png')


background = 255, 226, 191
pygame.init()

level= start_game()
game = game('my_levels',level)
size = game.load_size()
screen = pygame.display.set_mode(size)

#agent actions
#actions = ['DOWN', 'LEFT','UP','RIGHT']	
a1 = Agent(1)		
a2 = Agent(2)

while 1:
    time.sleep(0.5)

    if game.is_completed(): display_end(screen)
    print_game(game.get_matrix(),screen)
    
    #one agent
    #if game_option == 'Y':
    
    #RANDOM AGENT
    #Agent1
    
    action = random.choice(a1.actions())	
    if action == 'UP': game.move(0,-1, True, a1)
    elif action == 'DOWN': game.move(0,1, True, a1)
    elif action == 'LEFT': game.move(-1,0, True,  a1)
    elif action == 'RIGHT': game.move(1,0, True,  a1)

    #Agent2

    action = random.choice(a2.actions())	
    if action == 'UP': game.move(0,-1, True, a2)
    elif action == 'DOWN': game.move(0,1, True, a2)
    elif action == 'LEFT': game.move(-1,0, True,  a2)
    elif action == 'RIGHT': game.move(1,0, True,  a2)
    





    """
   # elif game_option == 'X':
   #USER INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            #USER INPUT
            
            #Agent1
            #if event.key == pygame.K_UP: game.move(0,-1, True, a1)
            #elif event.key == pygame.K_DOWN: game.move(0,1, True, a1)
            #elif event.key == pygame.K_LEFT: game.move(-1,0, True, a1)
            #elif event.key == pygame.K_RIGHT: game.move(1,0, True,  a1)
                
            #Agent2
            #if event.key == pygame.K_w: game.move(0,-1, True, a2)
            #elif event.key == pygame.K_s: game.move(0,1, True, a2)
            #elif event.key == pygame.K_a: game.move(-1,0, True,  a2)
            #elif event.key == pygame.K_d: game.move(1,0, True,  a2)
            
            #
            #elif event.key == pygame.K_q: sys.exit(0)
            #elif event.key == pygame.K_t: game.unmove(game.agent())
            #elif event.key == pygame.K_y: game.unmove(game.agent1())
     """       
    pygame.display.update()