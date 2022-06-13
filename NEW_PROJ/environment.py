from logging import raiseExceptions
import sys
import pygame
import string
import queue
import random
import time
from agent import Agent
#from viewer import *
from consts import BLACK,RED,BLUE
from functions import is_valid_value
from QL13 import puzzle13
from QL2_new import puzzle2


class game:
    
    box_in_dock_a1 = False
    box_in_dock_a2 = False
    def is_valid_value(self,char):
        if ( char == ' 'or #floor
            char == '#' or #wall
            
            char == '@' or #agent1
            char == '=' or #agent2
            
            char == '+' or #agent1 on dock
            char == '-' or #agent2 on dock           
            char == '.' or #button
            
            char == '*' or #box on right place 
            char == '!' or #box on wrong place 

            char == '$' or #barrier
            char == '%' or #dividing wall
            
            char == '1' or #num1
            char == '2' or #num2
            char == '3' or #num3
            char == '4' or #num4
            char == '5' or #num5

            char == 'a' or #box on dock_num1
            char == 'b' or #box on dock_num2
            char == 'c' or #box on dock_num3
            char == 'd' or #box on dock_num4
            char == 'e' or #box on dock_num5
            char == 'p' or #box 2 on . dock
            char == 'o' or #box 3 on . dock
            char == 'l' or #agent1 on number docks
            char == 'm' or #agent2 on number docks
            char == 'z' #finish
            ):
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
            if len(row) > x:
                x = len(row)
        return (x * 32, y * 32 + 90)

    def get_matrix(self):
        return self.matrix

    def print_matrix(self):
        for row in self.matrix:
            for char in row:
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write('\n')

    def is_completed(self):
        for row in self.matrix:
            for cell in row:
                if cell == 'z':
                    return False
        return True



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
                    if row[i] == '@' or row[i] == '+' or row[i] =='l':
                        return (x, y, row[i])
                    else:
                        x = x + 1
                y = y + 1
                x = 0

        elif agent.id ==2:
            
            for row in self.matrix:
                for i in range(6):
                    if row[i+5] == '=' or row[i+5] == '-' or row[i+5] == 'm':
                        return (x, y, row[i+5])
                    else:
                        x = x + 1
                y = y + 1
                x = 5

        else:
            raiseExceptions
            print("Invalid Id")


    def can_move(self,x,y, agent):
        return self.get_content(agent[0]+x,agent[1]+y) not in ['%','#','*', '$','1','2','3','4','5', '!','o','p']

    def next(self,x,y, agent ):
        return self.get_content(agent[0]+x,agent[1]+y)
    """
    def open_obstacle_agent(self,x,y, agent):
        return (self.next(x,y,agent) in ['.'])
    """
    def can_push(self,x,y,agent):
        #agent can only push boxes up or down
        if x != 0:
            return False
        elif (y<0 and agent[1] <=10) or (y>0 and agent[1]>=13) :
            return False
        else:
            options = ['1','2','3','4','5','!','o','p']#boxes and boxes in dock
            boxes_in_dock = ['a','b','c','d','e', ' ','.'] #boxes and floor 
            return (self.next(x,y,agent) in options and self.next(x+x,y+y,agent) in boxes_in_dock)

    
    def move_box(self,x,y,a,b):
#        (x,y) -> move to do
#        (a,b) -> box to move
        current_box = self.get_content(x,y)
        future_box = self.get_content(x+a,y+b)
        boxes = ['1','2','3','4','5']
        boxes_in_dock = ['a','b','c','d','e']
        if current_box == '!':
            if(x == 1 ):
                self.set_content(x+a,y+b,'1')
                self.set_content(x,y,'a')
            elif(x == 3 ):
                self.set_content(x+a,y+b,'3')
                self.set_content(x,y,'c')
            elif(x == 4 ):
                self.set_content(x+a,y+b,'4')
                self.set_content(x,y,'d')
            elif(x == 6 ):
                self.set_content(x+a,y+b,'5')
                self.set_content(x,y,'b')
            else:
                self.set_content(x+a,y+b,'2')
                self.set_content(x,y,'e')


        elif current_box in boxes and future_box == ' ':
            self.set_content(x+a,y+b,current_box)
            self.set_content(x,y,' ')

        elif current_box in boxes and future_box in boxes_in_dock:
            self.set_content(x+a,y+b,'*') #same 
            self.set_content(x,y,' ')
            

        elif current_box == '*' and future_box == ' ':
            self.set_content(x+a,y+b,current_box)
            self.set_content(x,y,boxes_in_dock)

        elif current_box == '*' and future_box in boxes_in_dock:
            self.set_content(x+a,y+b,'*')
            self.set_content(x,y,boxes_in_dock)
        elif current_box in boxes and future_box == '.':
            if(current_box == '2'):
                self.set_content(x+a,y+b,'p') #same 
                self.set_content(x,y,' ')
            else:
                self.set_content(x+a,y+b,'o') #same 
                self.set_content(x,y,' ')
        elif current_box in ['p','o'] and future_box == ' ':
            if(current_box == 'p'):
                self.set_content(x+a,y+b,'2') #same 
                self.set_content(x,y,'.')
            else:
                self.set_content(x+a,y+b,'3') #same 
                self.set_content(x,y,'.')

                
    def reset(self):
        self.box_in_dock_a1 = False
        self.box_in_dock_a2 = False
        self.last_box = ''
        self.puzzle2= False
        self.a1_dock = False
        self.a2_dock = False
        self.__init__('levels',1)



   
    def move(self,x,y,save, agent):
        docks = ['a','b','c','d','e']
        agent_position = self.agent_position(agent)
  
        if self.can_move(x,y, agent_position):
            current = agent_position
            future = self.next(x,y,agent_position)
            boxes = ['1','2','3','4','5']
            boxes_in_dock = ['a','b','c','d','e'] 

            if (current[2] == '@' or current[2] == '=') and future == ' ':
                self.set_content(current[0]+x,current[1]+y,current[2])
                self.set_content(current[0],current[1],' ')
            
            elif (current[2] == '@' or current[2] == '=') and future in '.':
    
                if agent.id == 1:
                    self.set_content(current[0]+x,current[1]+y,'+')
                    for i in range(0,5):
                        if(self.get_content(i,15) == '$'): # this has to be changes if wall is moved!!
                            self.set_content(i,15,' ')

                elif agent.id == 2:
                    self.set_content(current[0]+x,current[1]+y,'-')
                    for i in range(6,11):
                        if(self.get_content(i,15) == '$'): # this has to be changes if wall is moved!!
                            self.set_content(i,15,' ')

                self.set_content(current[0],current[1],' ')
            
            
            elif (current[2] == '+' or current[2] == '-') and future == ' ':
                if agent.id == 1:
                    self.a1_dock = False
                    self.set_content(current[0]+x,current[1]+y,'@')
                elif agent.id == 2:
                    self.a2_dock = False
                    self.set_content(current[0]+x,current[1]+y,'=')

                self.set_content(current[0],current[1],'.')
            #agent stepping on colored dock
            elif (current[2] == '@' or current[2] == '=') and future in docks:
    
                if agent.id == 1:
                    self.set_content(current[0]+x,current[1]+y,'l')
                elif agent.id == 2:
                   self.set_content(current[0]+x,current[1]+y,'m')
                self.set_content(current[0],current[1],' ')

            #agent on colored docks
            elif (current[2] == 'l' or current[2] == 'm') and future == ' ':
                if agent.id == 1:
                  
                    self.set_content(current[0]+x,current[1]+y,'@')
                elif agent.id == 2:
              
                    self.set_content(current[0]+x,current[1]+y,'=')

                if(current[0] == 1 ):
                    self.set_content(current[0],current[1],'a')
                elif(current[0] == 3 ):
                    self.set_content(current[0],current[1],'c')
                elif(current[0] == 4 ):
                    self.set_content(current[0],current[1],'d')
                elif(current[0] == 6 ):
                    self.set_content(current[0],current[1],'b')
                else:
                    self.set_content(current[0],current[1],'e')
            #agent step on colored dock to other colored dock
            elif (current[2] == 'l' or current[2] == 'm') and future in docks:
                if agent.id == 1:
                  
                    self.set_content(current[0]+x,current[1]+y,'l')
                elif agent.id == 2:
              
                    self.set_content(current[0]+x,current[1]+y,'m')

                if(current[0] == 1 ):
                    self.set_content(current[0],current[1],'a')
                elif(current[0] == 3 ):
                    self.set_content(current[0],current[1],'c')
                elif(current[0] == 4 ):
                    self.set_content(current[0],current[1],'d')
                elif(current[0] == 6 ):
                    self.set_content(current[0],current[1],'b')
                else:
                    self.set_content(current[0],current[1],'e')

                #if save: self.queue.put((x,y,False))

            elif (current[2] == '+' or current[2] == '-') and future == boxes_in_dock:
                self.set_content(current[0]+x,current[1]+y,current[2])
                self.set_content(current[0],current[1],boxes_in_dock)
                #if save: self.queue.put((x,y,False))
            

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
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,current[2])
                        
                    
                #if save: self.queue.put((x,y,True))
            
            elif (current[2] == '@' or current[2] == '=') and future in boxes and future_box in boxes_in_dock:

                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,current[2])
                if(agent.id == 1):
                    if(self.box_in_dock_a1):
                        #opens wall
                         for i in range(0,5):
                            if(self.get_content(i,8) == '$'): # this has to be changes if wall is moved!!
                                self.set_content(i,8,' ')
                    else:
                        self.box_in_dock_a1 =True
                elif(agent.id == 2):
                    if(self.box_in_dock_a2):
                        #opens wall
                        for i in range(6,11):
                            if(self.get_content(i,8) == '$'): # this has to be changes if wall is moved!!
                                self.set_content(i,8,' ')

                    else:
                        self.box_in_dock_a2 =True
                #if save: self.queue.put((x,y,True))
            elif (current[2] == '@' or current[2] == '=') and future == '*' and future_box == ' ':

                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                if agent.id == 1:
                    self.set_content(current[0]+x,current[1]+y,'+')
                elif agent.id == 2:
                    self.set_content(current[0]+x,current[1]+y,'-')
       
                #if save: self.queue.put((x,y,True))
            elif (current[2] == '@' or current[2] == '=') and future == '*' and future_box in boxes_in_dock:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                if agent.id == 1:
                    self.set_content(current[0]+x,current[1]+y,'+')
                elif agent.id == 2:
                    self.set_content(current[0]+x,current[1]+y,'-')
                #if save: self.queue.put((x,y,True))
            if (current[2] == '+' or current[2] == '-') and future in boxes and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                if agent.id == 1:
                    self.set_content(current[0]+x,current[1]+y,'@')
                elif agent.id == 2:
                    self.set_content(current[0]+x,current[1]+y,'=')
       
                #if save: self.queue.put((x,y,True))
            elif (current[2] == '+' or current[2] == '-') and future in boxes and future_box in boxes_in_dock:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],boxes_in_dock[boxes.index(future)])
                self.set_content(current[0]+x,current[1]+y,current[2])

                #if save: self.queue.put((x,y,True))
            elif (current[2] == '+' or current[2] == '-') and future == '*' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],boxes_in_dock)
                self.set_content(current[0]+x,current[1]+y,current[2])
                #if save: self.queue.put((x,y,True))
            elif (current[2] == '+' or current[2] == '-') and future == '*' and future_box in boxes_in_dock:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],boxes_in_dock)
                self.set_content(current[0]+x,current[1]+y,current[2])
                #if save: self.queue.put((x,y,True))
            elif (current[2] == '@' or current[2] == '=') and future == '!' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                if agent.id == 1:
                    self.set_content(current[0]+x,current[1]+y,'l')
                elif agent.id == 2:
                    self.set_content(current[0]+x,current[1]+y,'m')

            elif (current[2] == 'l' or current[2] == 'm') and future in boxes and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                if(current[0] == 1 ):
                    self.set_content(current[0],current[1],'a')
                elif(current[0] == 3 ):
                    self.set_content(current[0],current[1],'c')
                elif(current[0] == 4 ):
                    self.set_content(current[0],current[1],'d')
                elif(current[0] == 6 ):
                    self.set_content(current[0],current[1],'b')
                else:
                    self.set_content(current[0],current[1],'e')
            
                if agent.id == 1:
                    self.set_content(current[0]+x,current[1]+y,'@')
                elif agent.id == 2:
                    self.set_content(current[0]+x,current[1]+y,'=')
        
            elif (current[2] == '@' or current[2] == '=') and future in boxes and future_box == '.':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,current[2])
            elif (current[2] == '@' or current[2] == '=') and future in ['o','p'] and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                if agent.id == 1:
                    self.set_content(current[0]+x,current[1]+y,'+')
                elif agent.id == 2:
                    self.set_content(current[0]+x,current[1]+y,'-')
        agent_position = None    

def print_game(matrix,screen):

    screen.fill(background)
    x = 0
    y = 0
    for row in matrix:
        for char in row:
            if char == '%': #dividing_wall
                screen.blit(dividing_wall,(x,y)) 
            elif char == '#': #wall
                screen.blit(wall,(x,y))

            elif char == '=': #agent2
                screen.blit(agent1,(x,y)) 
            elif char == '@': #agent1 
                screen.blit(agent,(x,y))
            elif char == 'l':
                screen.blit(agent,(x,y)) #agent1 on numbered dock
            elif char == 'm':
                screen.blit(agent1,(x,y)) #agent2 on numbered dock
            if char == ' ': #floor
                screen.blit(floor,(x,y))
 

            elif char == '.': #button
                screen.blit(docker,(x,y))

            elif char == '*': #box on right place
                screen.blit(box_right_place,(x,y))
            elif char == '!': #box on wrong place
                screen.blit(box_wrong_place,(x,y))

            elif char == '$': #barrier
                screen.blit(box,(x,y))

            elif char == '+': #agent1 on dock
                screen.blit(agent_docked,(x,y))
            elif char == '-': #agent2 on dock
                screen.blit(agent1_docked,(x,y))

            elif char == '1': #num1
                screen.blit(box_wrong_place,(x,y))
            elif char == '2': #num2
                screen.blit(box_wrong_place,(x,y))
            elif char == '3': #num3
                screen.blit(box_wrong_place,(x,y))
            elif char == '4': #num4
                screen.blit(box_wrong_place,(x,y))
            elif char == '5': #num5
                screen.blit(box_wrong_place,(x,y))

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


            elif char == 'p': #box2 on dock .
                screen.blit(num2,(x,y))
            elif char == 'o':  #box3 on dock .
                screen.blit(num3,(x,y))

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



def display_end(screen):
    message = "Level Completed"
    fontobject = pygame.font.Font(None,18)
    pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 50,
                    200,20), 0)
    pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 60, (screen.get_height() / 2) - 90))
    pygame.display.flip()

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    450,30), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 300,
                    (screen.get_height() / 2) - 12,
                    620,18), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 300, (screen.get_height() / 2) - 10))
  pygame.display.flip()


def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + "  : " + "".join(current_string)
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
    display_box(screen, question + " >>  " + "".join(current_string)
)
  return "".join(current_string)


def agentType():
    start = pygame.display.set_mode((660,240))

    #game_option = ask(pygame.display.set_mode((320,1500)),"Game option: \nX: one agent\n Y: agent1 vs agent2\n Z: user vs agent2")

    agent_type = ask(start,"OPTION:  1) User Vs Random Agent  2) User Vs Q-Learning Agent   3) Q-Learning Agent  Vs  Random")
    if int(agent_type) > 0 and int(agent_type)<=3: # and (game_option=='X' or game_option=='Y' or game_option=='Z'):
        return agent_type #, game_option
    else:
        print("ERROR: Invalid Level or game option: "+str(agent_type))
        sys.exit(2)




    
dividing_wall = pygame.image.load('images/wall1.png')
agent1 = pygame.image.load('images/agent1.png')
wall = pygame.image.load('images/wall.png')
floor = pygame.image.load('images/floor.png')
box = pygame.image.load('images/bomx.png')
box_right_place = pygame.image.load('images/box_docked.png')
box_wrong_place = pygame.image.load('images/box_docked_wrong.png')
agent = pygame.image.load('images/agent.png')
agent_docked = pygame.image.load('images/agent_dock.png')
agent1_docked = pygame.image.load('images/agent_dock1.png')
docker = pygame.image.load('images/dock.png')
num1 = pygame.image.load('images/n1.png')
num2 = pygame.image.load('images/n2.png')
num3 = pygame.image.load('images/n3.png')
num4 = pygame.image.load('images/n4.png')
num5 = pygame.image.load('images/n5.png')
dock_num1 = pygame.image.load('images/dock_n1.png')
dock_num2 = pygame.image.load('images/dock_n1.png')
dock_num3 = pygame.image.load('images/dock_n1.png')
dock_num4 = pygame.image.load('images/dock_n1.png')
dock_num5 = pygame.image.load('images/dock_n1.png')
finish = pygame.image.load('images/finish.png')


background = 255, 226, 191
pygame.init()

agent_type= agentType()
game = game('levels',1) #level1
size = game.load_size()
screen = pygame.display.set_mode(size)
steps_A1 = 0
steps_A2 = 0
#agent actions
#actions = ['DOWN', 'LEFT','UP','RIGHT']	
clock = pygame.time.Clock()
all_sprites_list = pygame.sprite.Group()
a1 = Agent(1)		
a2 = Agent(2)
p1 = True
p2 = False
p3 = False
puzzle1 = puzzle13("./puzzle_splitted1.txt", (3, 1))
puzzle_2= puzzle2("./puzzle_splited2.txt")
puzzle_3 = puzzle13("./puzzle_splitted3.txt", (3, 1))
while 1:
    if game.is_completed():
        game.reset()
        
    #
    clock = pygame.time.Clock()
    #Initialise player scores
    steps_A1 = 0
    steps_A2 = 0

    print_game(game.get_matrix(),screen)
    if int(agent_type) ==1:
        #Agent1 -> User input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                #USER INPUT
                #Agent1
                if event.key == pygame.K_UP: 
                    game.move(0,-1, True, a1)
                    steps_A1 +=1
                elif event.key == pygame.K_DOWN: 
                    game.move(0,1, True, a1)
                    steps_A1 +=1
                elif event.key == pygame.K_LEFT: 
                    game.move(-1,0, True, a1)
                    steps_A1 +=1
                elif event.key == pygame.K_RIGHT:
                    game.move(1,0, True,  a1)
                    steps_A1 +=1
            #TODO -> end of second puzzle
            if game.box_in_dock_a1:
                    print("OK!")
                    text = font.render(str(steps_A1), 1, BLACK)
                    screen.blit(text, (5,684)) 
            if game.box_in_dock_a2:
                    text = font.render(str(steps_A2), 1, BLACK)
                    screen.blit(text, (5,704)) 

        #Agent2 -> Random
        action = random.choice(a2.actions())	
        if action == 'UP': 
            game.move(0,-1, True, a2)
            steps_A2 +=1
        elif action == 'DOWN': 
            game.move(0,1, True, a2)
            steps_A2 +=1
        elif action == 'LEFT': 
            game.move(-1,0, True,  a2)
            steps_A2 +=1
        elif action == 'RIGHT': 
            game.move(1,0, True,  a2)
            steps_A2 +=1 


    elif int(agent_type) ==2:
        #Agent1 -> User input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                #USER INPUT
                #Agent1
                if event.key == pygame.K_UP: 
                    game.move(0,-1, True, a1)
                    steps_A1 +=1
                elif event.key == pygame.K_DOWN: 
                    game.move(0,1, True, a1)
                    steps_A1 +=1
                elif event.key == pygame.K_LEFT: 
                    game.move(-1,0, True, a1)
                    steps_A1 +=1
                elif event.key == pygame.K_RIGHT:
                    game.move(1,0, True,  a1)
                    steps_A1 +=1
        #TODO

    elif int(agent_type) ==3:
        #Agent1 -> Random
        #time.sleep(0.1)

        '''
        action = random.choice(a1.actions())	
        if action == 'UP': 
            game.move(0,-1, True, a1)
            steps_A1 +=1
        elif action == 'DOWN': 
            game.move(0,1, True, a1)
            steps_A1 +=1
        elif action == 'LEFT': 
            game.move(-1,0, True,  a1)
            steps_A1 +=1
        elif action == 'RIGHT': 
            game.move(1,0, True,  a1)
            steps_A1 +=1
         '''
        #Agent2 -> Q-Learning
        #TODO
        #puzzle1
        if p1:
            print("p1")
            action,win, cost =  puzzle1.run_one(0)
            if action == 'UP': 
                game.move(0,-1, True, a2)
                steps_A2 +=1
            elif action == 'DOWN': 
                game.move(0,1, True, a2)
                steps_A2 +=1
            elif action == 'LEFT': 
                game.move(-1,0, True,  a2)
                steps_A2 +=1
            elif action == 'RIGHT': 
                game.move(1,0, True,  a2)
                steps_A2 +=1
            if win:
                puzzle1.change_init_position( (3, 1))
                p1 = False
                p2 = True
        
        if p2:
            action, win, cost, pos = puzzle_2.run_one(0)
            print("p2")
            if action == 'UP': 
                game.move(0,-1, True, a2)
                steps_A2 +=1
            elif action == 'DOWN': 
                game.move(0,1, True, a2)
                steps_A2 +=1
            elif action == 'LEFT': 
                game.move(-1,0, True,  a2)
                steps_A2 +=1
            elif action == 'RIGHT': 
                game.move(1,0, True,  a2)
                steps_A2 +=1
            if win:
                p2 = False
                p3 = True
                puzzle_3.change_init_position((12,pos[1]))
                puzzle_2.reset()


        if p3:
            print("p3")
            action, win, cost = puzzle_3.run_one(0)
            
            if action == 'UP': 
                game.move(0,-1, True, a2)
                steps_A2 +=1
            elif action == 'DOWN': 
                game.move(0,1, True, a2)
                steps_A2 +=1
            elif action == 'LEFT': 
                game.move(-1,0, True,  a2)
                steps_A2 +=1
            elif action == 'RIGHT': 
                game.move(1,0, True,  a2)
                steps_A2 +=1
            if win:
                p1 = True
                p2 = False
                p3 = False
                print("VOITTO")
                game.reset()




    #Display scores:
    font = pygame.font.Font(None, 18)
    #Agent1
    text = font.render(str("Agent_1"), 1, BLUE)
    screen.blit(text, (5,644)) 
    text = font.render(str("Time"), 1, BLACK)
    screen.blit(text, (60,644))   
    text = font.render(str("Steps"), 1, BLACK)
    screen.blit(text, (120,644)) 

    text = font.render(str("Puzzle_1"), 1, BLACK)
    screen.blit(text, (5,664)) 
    text = font.render(str("Puzzle_2"), 1, BLACK)
    screen.blit(text, (5,684)) 
    text = font.render(str("Puzzle_3"), 1, BLACK)
    screen.blit(text, (5,704)) 
    #Agent2
    text = font.render(str("Agent_2"), 1, RED)
    screen.blit(text, (195,644)) 
    text = font.render(str("Time"), 1, BLACK)
    screen.blit(text, (250,644))   
    text = font.render(str("Steps"), 1, BLACK)
    screen.blit(text, (310,644)) 

    text = font.render(str("Puzzle_1"), 1, BLACK)
    screen.blit(text, (195,664)) 
    text = font.render(str("Puzzle_2"), 1, BLACK)
    screen.blit(text, (195,684)) 
    text = font.render(str("Puzzle_3"), 1, BLACK)
    screen.blit(text, (195,704)) 
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)
    #-------------------------------------------------






    #RANDOM AGENT
    #Agent1
    """     action = random.choice(a1.actions())	
    if action == 'UP': 
        game.move(0,-1, True, a1)
    
        steps_A1 +=1
    elif action == 'DOWN': 
        game.move(0,1, True, a1)
        steps_A1 +=1
    elif action == 'LEFT': 
        game.move(-1,0, True,  a1)
        steps_A1 +=1
    elif action == 'RIGHT': 
        game.move(1,0, True,  a1)
        steps_A1 +=1
    
    #Agent2
    action = random.choice(a2.actions())	
    if action == 'UP': 
        game.move(0,-1, True, a2)
        steps_A2 +=1
    elif action == 'DOWN': 
        game.move(0,1, True, a2)
        steps_A2 +=1
    elif action == 'LEFT': 
        game.move(-1,0, True,  a2)
        steps_A2 +=1
    elif action == 'RIGHT': 
        game.move(1,0, True,  a2)
        steps_A2 +=1 """
    
    #USER INPUT
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            #USER INPUT
            #Agent1
            if event.key == pygame.K_UP: game.move(0,-1, True, a1)
            elif event.key == pygame.K_DOWN: game.move(0,1, True, a1)
            elif event.key == pygame.K_LEFT: game.move(-1,0, True, a1)
            elif event.key == pygame.K_RIGHT: game.move(1,0, True,  a1)
                
            #Agent2
            if event.key == pygame.K_w: game.move(0,-1, True, a2)
            elif event.key == pygame.K_s: game.move(0,1, True, a2)
            elif event.key == pygame.K_a: game.move(-1,0, True,  a2)
            elif event.key == pygame.K_d: game.move(1,0, True,  a2)
            
            #
            #elif event.key == pygame.K_q: sys.exit(0)
            #elif event.key == pygame.K_t: game.unmove(game.agent())
            #elif event.key == pygame.K_y: game.unmove(game.agent1())
     """
    pygame.display.update()