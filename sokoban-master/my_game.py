#!../bin/python

import sys
import pygame
import string
import queue

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

    def agent(self):
        x = 0
        y = 0
        for row in self.matrix:
            
            for pos in row:
                if pos == '@' or pos == '+':
                    return (x, y, pos)
                else:
                    x = x + 1
            y = y + 1
            x = 0

    def agent1(self):
        x = 0
        y = 0
        for row in self.matrix:
            for pos in row:
                if pos == '='or pos == '+':
                    return (x, y, pos)
                else:
                    x = x + 1
            y = y + 1
            x = 0

    def can_move(self,x,y, agent):
        agent = agent
        return self.get_content(agent[0]+x,agent[1]+y) not in ['%','#','*','$']

    def next(self,x,y, agent ):
        agent = agent
        return self.get_content(agent[0]+x,agent[1]+y)
    """
    def open_obstacle_agent(self,x,y, agent):
        return (self.next(x,y,agent) in ['.'])
    """


    def can_push(self,x,y,agent):
        return (self.next(x,y,agent) in ['*','$'] and self.next(x+x,y+y,agent) in [' ','.'])

    def is_completed(self):
        for row in self.matrix:
            for cell in row:
                if cell == '$':
                    return False
        return True





    def move(self,x,y,save,  agent_id, agent = None,):
        print()
        print(" X",x," Y",y)

        print("A: ", self.agent())
        agent = agent
        
        if self.can_move(x,y, agent):
            current = agent
            #print("get content ",self.get_content(agent[0]+x,agent[1]+y) )
            future = self.next(x,y,agent)
            print("FUTURE ", future)
            print("agent0 ", self.agent())
            print("agent1 ", self.agent1())
            print("current: ",current[0], " current[1]: ", current[1] )
            print("current[0]+x: ",current[0]+x, " current[1]+y: ", current[1]+y)

            if (current[2] == '@' or current[2] == '=') and future == ' ':
                self.set_content(current[0]+x,current[1]+y,current[2])
                self.set_content(current[0],current[1],' ')
                if save: self.queue.put((x,y,False))
            
            elif (current[2] == '@' or current[2] == '=') and future == '.':
                
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],' ')
                
                #OBSTACLE 1

                for x in range(3): #meter 10
                    if(self.get_content(x,current[1]+y-1) == '$'):
                        self.set_content(x,current[1]+y-1,' ')


            
            elif current[2] == '+' and future == ' ':
                if agent_id == 0:
                    self.set_content(current[0]+x,current[1]+y,'@')
                elif agent_id == 1:
                    self.set_content(current[0]+x,current[1]+y,'=')

                self.set_content(current[0],current[1],'.')
                #if save: self.queue.put((x,y,False))

            elif current[2] == '+' and future == '.':
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],'.')

                #if save: self.queue.put((x,y,False))
        





def print_game(matrix,screen):
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
    level = ask(start,"Select Level")
    if int(level) > 0:
        return level
    else:
        print("ERROR: Invalid Level: "+str(level))
        sys.exit(2)
dividing_wall = pygame.image.load('images/wall1.png')
agent1 = pygame.image.load('images/agent1.png')

wall = pygame.image.load('images/wall.png')
floor = pygame.image.load('images/floor.png')
box = pygame.image.load('images/box.png')
box_docked = pygame.image.load('images/box_docked.png')
agent = pygame.image.load('images/agent.png')
agent_docked = pygame.image.load('images/agent_dock.png')
docker = pygame.image.load('images/dock.png')
background = 255, 226, 191
pygame.init()

level = start_game()
game = game('my_levels',level)
size = game.load_size()
screen = pygame.display.set_mode(size)
while 1:
    if game.is_completed(): display_end(screen)
    print_game(game.get_matrix(),screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            #Agent
            if event.key == pygame.K_UP: game.move(0,-1, True,0 , game.agent())
            elif event.key == pygame.K_DOWN: game.move(0,1, True,0 , game.agent())
            elif event.key == pygame.K_LEFT: game.move(-1,0, True,0 ,  game.agent())
            elif event.key == pygame.K_RIGHT: game.move(1,0, True,0 ,  game.agent())
            
            #Agent1
            if event.key == pygame.K_w: game.move(0,-1, True,1 ,  game.agent1())
            elif event.key == pygame.K_s: game.move(0,1, True,1 , game.agent1())
            elif event.key == pygame.K_a: game.move(-1,0, True,1 ,  game.agent1())
            elif event.key == pygame.K_d: game.move(1,0, True,1 ,  game.agent1())

            #
            elif event.key == pygame.K_q: sys.exit(0)
            #elif event.key == pygame.K_t: game.unmove(game.agent())
            #elif event.key == pygame.K_y: game.unmove(game.agent1())

    pygame.display.update()