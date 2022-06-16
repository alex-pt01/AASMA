import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functions import get_coordinates_puzzle2
import time

class puzzle2_SARSA:
    def __init__(self,filename):
        self.filename = filename
        self.actions = ["LEFT", "RIGHT", "UP", "DOWN"]
        self.length =  get_coordinates_puzzle2(filename)[0]
        self.width = get_coordinates_puzzle2(filename)[1]
        self.initial_agent_location = get_coordinates_puzzle2(filename)[2]
        self.wall_coordinates = get_coordinates_puzzle2(filename)[3]
        self.agent_location =  self.initial_agent_location
        self.boxes = get_coordinates_puzzle2(filename)[4]
        self.box1_location = get_coordinates_puzzle2(filename)[4][0]
        self.box2_location = get_coordinates_puzzle2(filename)[4][1]
        #self.dock_location =  get_coordinates_puzzle2(filename)[5]
        self.dock1 = get_coordinates_puzzle2(filename)[5][0]
        self.dock2 = get_coordinates_puzzle2(filename)[5][1]
        self.init_walls = get_coordinates_puzzle2(filename)[3]
        self.init_box =  get_coordinates_puzzle2(filename)[4]
        self.init_box1_location = get_coordinates_puzzle2(filename)[4][0]
        self.init_box2_location = get_coordinates_puzzle2(filename)[4][1]
        self.shortest = []
        self.remember = []
        self.key = 0    
        self.discount =  0.9
        self.learning_rate =  0.9
        self.greedy = 0.9
        self.index = 0
        self.paths = []
        self.Q = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.final_Q = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.action = self.get_action(str(self.initial_agent_location))
        self.steps = []
        self.costs = []
        self.eps_min = 0.01
        self.eps_dec = 5e-4
        self.box1_in_dock = 0
        self.box2_in_dock = 0


    def reset(self):
        self.wall_coordinates = self.init_walls
        self.boxes = self.init_box
        self.box1_location = self.init_box1_location
        self.box2_location = self.init_box2_location
        self.box1_in_dock = 0
        self.box2_in_dock = 0
        self.agent_location = self.initial_agent_location

    def move(self,action):
        reward = -0.1
        '''
        print("vali1")
        print(self.box1_location)
        print(self.dock1)
        '''
        print("vali1")
        print(self.box1_location)
        print(self.dock1)
        print("vali2")
        print(self.box2_location)
        print(self.dock2)
        if action == "LEFT": 
            if (self.agent_location[0], self.agent_location[1]-1) not in self.wall_coordinates and (self.agent_location[0], self.agent_location[1]-1) != self.box1_location and (self.agent_location[0], self.agent_location[1]-1) != self.box2_location:
                self.agent_location = (self.agent_location[0], self.agent_location[1]-1)
        elif action == "RIGHT": 
            if (self.agent_location[0], self.agent_location[1]+1) not in self.wall_coordinates and  (self.agent_location[0], self.agent_location[1]+1) != self.box1_location and (self.agent_location[0], self.agent_location[1]+1) != self.box2_location:
                self.agent_location = (self.agent_location[0], self.agent_location[1]+1)
        elif action == "UP": 
            if  (self.agent_location[0]-1, self.agent_location[1]) not in self.wall_coordinates and (self.agent_location[0]-1, self.agent_location[1]) != self.box1_location and (self.agent_location[0]-1, self.agent_location[1]) != self.box2_location:
                self.agent_location = (self.agent_location[0]-1, self.agent_location[1])

            elif((self.agent_location[0]-1, self.agent_location[1]) == self.box1_location and self.box1_location[0] >3):
                print("push1")
             
                reward = 0.5
                self.agent_location = (self.agent_location[0]-1, self.agent_location[1])
                self.box1_location = (self.box1_location[0]-1, self.box1_location[1])
                if self.box1_location == self.dock1:
                    self.box1_in_dock = 1
                    reward = 5
                    #self.wall_coordinates.append(self.box1_location)
            
            elif((self.agent_location[0]-1, self.agent_location[1]) == self.box2_location and self.box2_location[0] >3):
                print("push2")
             
                reward = 0.5
                self.agent_location = (self.agent_location[0]-1, self.agent_location[1])
                self.box2_location = (self.box2_location[0]-1, self.box2_location[1])
                if self.box2_location == self.dock2:
                    self.box2_in_dock = 1
                    reward = 5
                    #self.wall_coordinates.append(self.box2_location)

        elif action == "DOWN": 
            if (self.agent_location[0]+1, self.agent_location[1]) not in self.wall_coordinates and   (self.agent_location[0]+1, self.agent_location[1]) != self.box1_location and (self.agent_location[0]+1, self.agent_location[1]) != self.box2_location:
                self.agent_location = (self.agent_location[0]+1, self.agent_location[1])

            elif((self.agent_location[0]+1, self.agent_location[1]) == self.box1_location):
                if(self.box1_location[0]+1 <= 6 and self.box1_in_dock != 1):
                   
                    reward = -1
                    self.box1_location = (self.box1_location[0]+1, self.box1_location[1])
                    self.agent_location = (self.agent_location[0]+1, self.agent_location[1])


            elif((self.agent_location[0]+1, self.agent_location[1]) == self.box2_location):
                if(self.box2_location[0]+1 <=  6 and self.box2_in_dock != 1):
                    
                    reward = -1
                    self.box2_location = (self.box2_location[0]+1, self.box2_location[1])
                    self.agent_location = (self.agent_location[0]+1, self.agent_location[1])


        self.remember.append(action)
        self.index +=1
        new_state = (self.agent_location[0],self.agent_location[1], self.box1_in_dock,self.box2_in_dock)
        print(self.box1_in_dock)
        print(self.box2_in_dock)
        if self.box1_in_dock == 1 and self.box2_in_dock == 1:
    
          
            reward = 10
            win = True
            self.paths.append(self.remember)
            if len(self.shortest)>len(self.remember) or len(self.shortest) == 0:
                self.shortest = self.remember
            self.remember = []
        else:
            win = False
         
        return new_state, reward, win


    def get_action(self,state):
        if state not in self.Q.index:#Muuta!!
             self.Q = self.Q.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.Q.columns,
                    name=state,
                )
            )

        random = np.random.uniform()
        if self.greedy < random:
            return np.random.choice(self.actions)

        else:
            state_action = self.Q.loc[state, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            return state_action.idxmax()


    def SarsaLearn(self, state, action, reward, next_action, next_state):
        #Verifies if State exists
        if next_state not in self.Q.index:
            self.Q = self.Q.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.Q.columns,
                    name=next_state,
                )
            )
        prediction = self.Q.loc[state,action]

        if next_state != 'goal' or next_state != 'obstacle':
            target = reward + self.discount * self.Q.loc[next_state, next_action]
        else:
            target = reward
        ''' Does not work for some reason
        if(self.greedy>self.eps_min):
            self.greedy-= self.eps_dec
        else:
            self.greedy = self.eps_min
        '''

        self.Q.loc[state, action] += self.learning_rate * (target - prediction)
        return self.Q.loc[state, action]

    def change_init_position(self, pos):
        self.initial_agent_location =pos
        self.agent_location = pos

    def run_puzzle(self, n): #muuta
 
        for i in range(n):
            state = self.initial_agent_location
            self.agent_location = self.initial_agent_location
            j = 0

            cost = 0

            running = True
            while running:  
               
                action = self.get_action(str(state))
                print(action)       
                next_state, reward, win = self.move(action)
                cost += self.SarsaLearn( str(state), action, reward,str(next_state))

                state = next_state

                j+=1

                if(win):
                    self.steps.append(i)
                    self.costs.append(cost)
                    running = False

    def run_one(self, c):
            state = self.agent_location   
            cost = c  
            next_action = self.get_action(str(state)) 
            next_state, reward, win = self.move(next_action)
            cost += self.SarsaLearn( str(state), self.action, reward,next_action, str(next_state))

            state = next_state
            self.action=next_action
            return next_action, win, cost

        





def main():
    puzzle = puzzle2_SARSA("./p_split2.txt")
    
    print(puzzle.run_puzzle(10))
    #print(puzzle.shortest)
if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()
