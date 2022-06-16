import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functions import get_coordinates_puzzle13


class puzzle13:
    def __init__(self,filename,init_agent_location):
        self.filename = filename
        self.actions = ["LEFT", "RIGHT", "UP", "DOWN"]
        self.length =  get_coordinates_puzzle13(filename)[0]
        self.width = get_coordinates_puzzle13(filename)[1]
        self.initial_agent_location = init_agent_location
        self.wall_coordinates = get_coordinates_puzzle13(filename)[3]
        self.agent_location =  init_agent_location
        self.goal = get_coordinates_puzzle13(filename)[4]
        self.shortest = []
        self.remember = []
        self.discount =  0.9
        self.learning_rate =  0.9
        self.greedy = 0.9
        self.paths = []
        self.Q = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.steps = []
        self.costs = []
        self.eps_max = 0.99
        self.eps_add = 5e-4

    def move(self,action):
        state = self.agent_location
        if action == "LEFT": 
            if (self.agent_location[0], self.agent_location[1]-1) not in self.wall_coordinates:
                self.agent_location = (self.agent_location[0], self.agent_location[1]-1)
        elif action == "RIGHT": 
            if (self.agent_location[0], self.agent_location[1]+1) not in self.wall_coordinates:
                self.agent_location = (self.agent_location[0], self.agent_location[1]+1)
        elif action == "UP":
            if  (self.agent_location[0]-1, self.agent_location[1]) not in self.wall_coordinates:
                self.agent_location = (self.agent_location[0]-1, self.agent_location[1])
        elif action == "DOWN": 
            if (self.agent_location[0]+1, self.agent_location[1]) not in self.wall_coordinates:
                self.agent_location = (self.agent_location[0]+1, self.agent_location[1])

        self.remember.append(action)
   
        new_state = self.agent_location 
        
        if new_state == self.goal:
            reward = 10
            win = True
            self.paths.append(self.remember)
            if len(self.shortest)>len(self.remember) or len(self.shortest) == 0:
                self.shortest = self.remember
            self.remember = []
        else:
            win = False
            reward = -0.1
         
        return new_state, reward, win


    def get_action(self,state):
        if state not in self.Q.index:
            self.Q = self.Q.append( pd.Series( [0,0,0,0], index=self.Q.columns,name=state, ) )


        random = np.random.uniform()
        if self.greedy < random:
            return np.random.choice(self.actions)

        else:
            state_action = self.Q.loc[state, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            return state_action.idxmax()


    def learn(self, state, action, reward, next_state):

        if next_state not in self.Q.index:
             self.Q = self.Q.append( pd.Series( [0,0,0,0], index=self.Q.columns,name=next_state ) )
        prediction = self.Q.loc[state,action]
            
        if next_state == self.goal:
            q = reward
        else:
            q = reward + self.discount * self.Q.loc[next_state, :].max() 
        
        if(self.greedy<self.eps_max):
            self.greedy+= self.eps_add
        else:
            self.greedy = self.eps_max
        
        self.Q.loc[state,action] += self.learning_rate * (q - prediction)
        return self.Q.loc[state, action]



    def run_puzzle(self, n): 
 
        for i in range(n):
            state = self.initial_agent_location
            self.agent_location = self.initial_agent_location
            j = 0

            cost = 0

            running = True
            while running:   
                action = self.get_action(str(state))       
                next_state, reward, win = self.move(action)
                cost += self.learn( str(state), action, reward,str(next_state))

                state = next_state

                j+=1

                if(win):
                    self.steps.append(i)
                    self.costs.append(cost)
                    running = False

    
    def change_init_position(self, pos):
        self.initial_agent_location =pos
        self.agent_location = pos

    def run_one(self, c):
            state = self.agent_location   
            cost = c  
            action = self.get_action(str(state))       
            next_state, reward, win = self.move(action)
            cost += self.learn( str(state), action, reward,str(next_state))

            state = next_state

            return action, win, cost




def main():
    puzzle = puzzle13("./puzzle_splitted3.txt", (12, 4))
    puzzle.run_puzzle(100)
    print(puzzle.shortest)
    plt.plot(1,[29])
    plt.plot(1,[50])
    plt.show()
if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()