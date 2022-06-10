import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functions import get_coordinates_puzzle13


class puzzle13:
    def __init__(self,filename,):
        self.filename = filename
        self.actions = ["Left", "Right", "Up", "Down"]
        self.length =  get_coordinates_puzzle13(filename)[0]
        self.width = get_coordinates_puzzle13(filename)[1]
        self.initial_player_location = get_coordinates_puzzle13(filename)[2]
        self.wall_coordinates = get_coordinates_puzzle13(filename)[3]
        self.player_location = get_coordinates_puzzle13(filename)[2]
        self.goal = get_coordinates_puzzle13(filename)[4]
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
        self.steps = []
        self.costs = []

    def move(self,action):
        state = self.player_location
        if action == "Left": #up
            if (self.player_location[0], self.player_location[1]-1) not in self.wall_coordinates:
                self.player_location = (self.player_location[0], self.player_location[1]-1)
        elif action == "Right": #down
            if (self.player_location[0], self.player_location[1]+1) not in self.wall_coordinates:
                self.player_location = (self.player_location[0], self.player_location[1]+1)
        elif action == "Up": #Left
            if  (self.player_location[0]-1, self.player_location[1]) not in self.wall_coordinates:
                self.player_location = (self.player_location[0]-1, self.player_location[1])
        elif action == "Down": #right
            if (self.player_location[0]+1, self.player_location[1]) not in self.wall_coordinates:
                self.player_location = (self.player_location[0]+1, self.player_location[1])

        self.remember.append(action)
        self.index +=1
        new_state = self.player_location 
        
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


    def learn(self, state, action, reward, next_state):#muuta koko paska
        if next_state not in self.Q.index:#Muuta!!
             self.Q = self.Q.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.Q.columns,
                    name=next_state,
                )
            )
        prediction = self.Q.loc[state,action]
            
        if next_state == self.goal:
            q_tar = reward
        else:
            q_tar = reward + self.discount * self.Q.loc[next_state, :].max() #Q lauseke

        self.Q.loc[state,action] += self.learning_rate * (q_tar - prediction)
        return self.Q.loc[state, action]



    def run_puzzle(self, n): #muuta
 
        for i in range(n):
            state = self.initial_player_location
            self.player_location = self.initial_player_location
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


def main():
    puzzle = puzzle13("./puzzle_splitted3.txt")
    puzzle.run_puzzle(100)
    print(puzzle.shortest)
if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()