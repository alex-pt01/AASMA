import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functions import get_coordinates_puzzle13


class puzzle13:
    def __init__(self,filename, actions = ["U", "D", "L", "R"],discount = 0.9 ,learning_rate =0.9, greedy=0.9 ):
        self.filename = filename
        self.actions = actions
        self.discount = discount
        self.learning_rate = learning_rate
        self.length =  get_coordinates_puzzle13(filename)[0]
        self.width = get_coordinates_puzzle13(filename)[1]
        self.initial_player_location = get_coordinates_puzzle13(filename)[2]
        self.wall_coordinates = get_coordinates_puzzle13(filename)[3]
        self.player_location = get_coordinates_puzzle13(filename)[2]
        self.goal = get_coordinates_puzzle13(filename)[4]
        self.final = []
        self.remember = []
        self.key = 0    
        self.shortest = 0
        self.longest = 0
        self.discount = discount
        self.learning_rate = learning_rate
        self.greedy = greedy
        self.index = 0

        self.Q = pd.DataFrame(columns=self.actions, dtype=np.float64)
        # Creating Q-table for cells of the final route
        self.final_Q = pd.DataFrame(columns=self.actions, dtype=np.float64)
        # change
        self.first = True


    def move(self,action):
        state = self.player_location
        if action == 'L': #up
            if (self.player_location[0], self.player_location[1]-1) not in self.wall_coordinates:
                self.player_location = (self.player_location[0], self.player_location[1]-1)
        elif action == 'R': #down
            if (self.player_location[0], self.player_location[1]+1) not in self.wall_coordinates:
                self.player_location = (self.player_location[0], self.player_location[1]+1)
        elif action == 'U': #Left
            if  (self.player_location[0]-1, self.player_location[1]) not in self.wall_coordinates:
                self.player_location = (self.player_location[0]-1, self.player_location[1])
        elif action == 'D': #right
            if (self.player_location[0]+1, self.player_location[1]) not in self.wall_coordinates:
                self.player_location = (self.player_location[0]+1, self.player_location[1])

        self.remember.append(action)
        self.index +=1
        new_state = self.player_location 
        
        if( new_state == self.goal):
            reward = 10
            win = True
            #Muuuta!!!
            if self.first == True:
                self.final = self.remember
                self.c = False
                self.longest = len(self.remember)
                self.shortest = len(self.remember)

            if len(self.remember) < len(self.final):
                # Saving the number of steps for the shortest route
                self.shortest = len(self.remember)
                # Clearing the dictionary for the final route
                self.final = {}
                # Reassigning the dictionary
                self.final = self.remember
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
        # Resulted list for the plotting Episodes via Steps
        steps = []
        # Summed costs for all episodes in resulted list
        all_costs = []
       
        for i in range(n):
            state = self.initial_player_location
            self.player_location = self.initial_player_location
            print("uusi")
            print(state)
            print(self.goal)
            j = 0

            cost = 0

            running = True
            while running:
                
                action = self.get_action(str(state))
                print(action)
                
                next_state, reward, win = self.move(action)
                print(next_state)
                cost += self.learn( str(state), action, reward,str(next_state))

                state = next_state

                i+=1

                if(win):
                    steps += [i]
                    all_costs += [cost]
                    running = False


def main():
    puzzle = puzzle13("./puzzle_splitted3.txt")
    puzzle.run_puzzle(300)
    print(puzzle.final)
if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()