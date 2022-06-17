import math
import numpy as np
  
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

import tensorflow as tf

from functions import get_coordinates_puzzle2

import time

class DeepQNetwork(nn.Module):
    def __init__(self, lr, input_dims, fc1_dims, fc2_dims,
                 n_actions):
        super(DeepQNetwork, self).__init__()
        self.input_dims = input_dims
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.n_actions = n_actions
        self.fc1 = nn.Linear(*self.input_dims, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
        self.fc3 = nn.Linear(self.fc2_dims, self.n_actions)
        
        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.loss = nn.MSELoss()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(self.device)

    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        actions = self.fc3(x)

        return actions

        
class DQNAgent2:
    def __init__(self, filename, gamma, epsilon, lr, input_dims, batch_size, n_actions):
        self.filename = filename
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_max = 0.99
        self.eps_add = 5e-4
        self.lr = lr
        self.action_space = [i for i in range(n_actions)]
        self.mem_size = 100000
        self.batch_size = batch_size
        self.mem_cntr = 0
        self.iter_cntr = 0
        self.replace_target = 100


        self.Q_eval = DeepQNetwork(lr, n_actions=n_actions,
                                   input_dims=input_dims,
                                   fc1_dims=256, fc2_dims=256)
        self.state_memory = np.zeros((self.mem_size, *input_dims),
                                     dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_dims),
                                         dtype=np.float32)
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.bool)
        self.init_observation =  get_coordinates_puzzle2(filename)[2]
        self.observation = get_coordinates_puzzle2(filename)[2]
        #Important Coordinates
        self.wall_coordinates = get_coordinates_puzzle2(filename)[3]
        #self.agent_location =  self.initial_agent_location
        self.boxes = get_coordinates_puzzle2(filename)[4]
        self.box1_location = (np.float32(get_coordinates_puzzle2(filename)[4][0][0]), np.float32(get_coordinates_puzzle2(filename)[4][0][1]))
        self.box2_location = (np.float32(get_coordinates_puzzle2(filename)[4][1][0]), np.float32(get_coordinates_puzzle2(filename)[4][1][1]))
        #self.dock_location =  get_coordinates_puzzle2(filename)[5]
        self.dock1 =(np.float32(get_coordinates_puzzle2(filename)[5][0][0]), np.float32(get_coordinates_puzzle2(filename)[5][0][1]))
        self.dock2 = (np.float32(get_coordinates_puzzle2(filename)[5][1][0]), np.float32(get_coordinates_puzzle2(filename)[5][1][1]))
        self.init_walls = get_coordinates_puzzle2(filename)[3]
        self.init_box =  get_coordinates_puzzle2(filename)[4]
        self.init_box1_location = (np.float32(get_coordinates_puzzle2(filename)[4][0][0]), np.float32(get_coordinates_puzzle2(filename)[4][0][1]))
        self.init_box2_location =  (np.float32(get_coordinates_puzzle2(filename)[4][1][0]), np.float32(get_coordinates_puzzle2(filename)[4][1][1]))
        self.box1_in_dock = 0
        self.box2_in_dock = 0
        self.shortest = []
        self.remember = []
        #self.initial_player_location = get_coordinates_puzzle13(filename)[2]

    def store_transition(self, state, action, reward, next_state, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = next_state
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.terminal_memory[index] = done

        self.mem_cntr +=1
    
    def choose_action(self, observation):
        if np.random.uniform() < self.epsilon:
            state = torch.tensor([observation]).to(self.Q_eval.device)
            actions = self.Q_eval.forward(state)
            action = torch.argmax(actions).item()
        else:
            print("random")
            action = np.random.choice(self.action_space)
        return action

    def learn(self):
        if self.mem_cntr < self.batch_size:
            return
        
        self.Q_eval.optimizer.zero_grad()

        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, self.batch_size, replace = False)

        batch_index = np.arange(self.batch_size, dtype=np.int32)

        state_batch = torch.tensor(self.state_memory[batch]).to(self.Q_eval.device)
        new_state_batch = torch.tensor(self.new_state_memory[batch]).to(self.Q_eval.device)
        reward_batch = torch.tensor(self.reward_memory[batch]).to(self.Q_eval.device)
        terminal_batch = torch.tensor(self.terminal_memory[batch]).to(self.Q_eval.device)
        action_batch = self.action_memory[batch]

        q_eval = self.Q_eval.forward(state_batch)[batch_index, action_batch]
        q_next = self.Q_eval.forward(new_state_batch)
        q_next[terminal_batch] = 0.0

        q_target = reward_batch + self.gamma * torch.max(q_next, dim=1)[0]

        loss = self.Q_eval.loss(q_target, q_eval).to(self.Q_eval.device)
        loss.backward()
        self.Q_eval.optimizer.step()


        
        if(self.epsilon<self.eps_max):
            self.epsilon += self.eps_add
        else:
            self.epsilon = self.eps_max
    
        

    def move(self,action):
            reward = -0.1
            pos = (self.observation[0], self.observation[1])
            if action ==0: 
                if (self.observation[0], self.observation[1]-1) not in self.wall_coordinates and (self.observation[0], self.observation[1]-1) != self.box1_location and (self.observation[0], self.observation[1]-1) != self.box2_location:
                    pos = (self.observation[0], self.observation[1]-1)
            elif action == 1: 
                if (self.observation[0], self.observation[1]+1) not in self.wall_coordinates and  (self.observation[0], self.observation[1]+1) != self.box1_location and (self.observation[0], self.observation[1]+1) != self.box2_location:
                    pos = (self.observation[0], self.observation[1]+1)
            elif action == 2: 
                if  (self.observation[0]-1, self.observation[1]) not in self.wall_coordinates and (self.observation[0]-1, self.observation[1]) != self.box1_location and (self.observation[0]-1, self.observation[1]) != self.box2_location:
              
                    pos = (self.observation[0]-1, self.observation[1])
                   
          
                elif((self.observation[0]-1, self.observation[1]) == self.box1_location and self.box1_location[0] >3):
                 
               
                    reward = 0.5
                    pos = (self.observation[0]-1, self.observation[1])
                    self.box1_location = (self.box1_location[0]-1, self.box1_location[1])
                    if self.box1_location == self.dock1:
                        self.box1_in_dock = 1
                        self.reward = 5
                    
                        #self.wall_coordinates.append(self.box1_location)
                
                elif((self.observation[0]-1, self.observation[1]) == self.box2_location and self.box2_location[0] >3):
                 
                
                    reward = 0.5
                    pos = (self.observation[0]-1, self.observation[1])
                    self.box2_location = (self.box2_location[0]-1, self.box2_location[1])
                    if self.box2_location == self.dock2:
                        self.box2_in_dock = 1
                        self.reward = 5
                        #self.wall_coordinates.append(self.box2_location)

            elif action == 3: 
                if (self.observation[0]+1, self.observation[1]) not in self.wall_coordinates and   (self.observation[0]+1, self.observation[1]) != self.box1_location and (self.observation[0]+1, self.observation[1]) != self.box2_location:
                    pos= (self.observation[0]+1.0, self.observation[1])

                elif((self.observation[0]+1, self.observation[1]) == self.box1_location):
                    if(self.box1_location[0]+1 <= 6 and self.box1_in_dock != 1):
                    
                        reward = -1
                        self.box1_location = (self.box1_location[0]+1, self.box1_location[1])
                        pos = (self.observation[0]+1, self.observation[1])


                elif((self.observation[0]+1, self.observation[1]) == self.box2_location):
                    if(self.box2_location[0]+1 <=  6 and self.box2_in_dock != 1):
                        
                        reward = -1
                        self.box2_location = (self.box2_location[0]+1, self.box2_location[1])
                        pos = (self.observation[0]+1, self.observation[1])
                        
            new_state =  (np.float32(pos[0]),np.float32(pos[1]), np.float32(self.box1_location[0]),np.float32(self.box1_location[1]), np.float32(self.box2_location[0]), np.float32(self.box2_location[1]))

            if self.box1_in_dock == 1 and self.box2_in_dock == 1:

                reward = 10
                win = True
                #self.paths.append(self.remember)
                if len(self.shortest)>len(self.remember) or len(self.shortest) == 0:
                    self.shortest = self.remember
                self.remember = []
            else:
                win = False

            return new_state, reward, win

    def run_puzzle(self, n): 
        scores, eps_history = [], []
        for i in range(n):
            done = False
            score = 0
            observation = get_coordinates_puzzle2(self.filename)[2]
            observation = (np.float32(self.observation[0]),np.float32(self.observation[0]), np.float32(self.box1_location[0]),np.float32(self.box1_location[1]), np.float32(self.box2_location[0]), np.float32(self.box2_location[1]))

            while not done:
                action = self.choose_action(observation)
                new_state, reward, done = self.move(action)
                print(reward)
                score += reward
                self.store_transition(observation, action, reward, new_state, done)
                observation = new_state
                self.learn()
            eps_history.append(self.epsilon)
            scores.append(score)

            avg_score = np.mean(scores[-100:])
            print('episode: ', i, 'score %.2f' % score,
                    'average_score %.2f' % avg_score,
                    'epsilon %.2f' % self.epsilon)

        #x = [i+1 for i in range(n)]
    def reset(self):
        self.wall_coordinates = self.init_walls
        self.boxes = self.init_box
        self.box1_location = self.init_box1_location
        self.box2_location = self.init_box2_location
        self.box1_in_dock = 0
        self.box2_in_dock = 0
        self.observation= self.init_observation

    def run_one(self,c):
        state = (self.observation[0],self.observation[1], np.float32(self.box1_location[0]),np.float32(self.box1_location[1]), np.float32(self.box2_location[0]), np.float32(self.box2_location[1]))
        action = self.choose_action(state)       
        next_state, reward, win = self.move(action)
        print(reward)
        cost = c+ reward
        pos = (next_state[0],next_state[1])
        self.store_transition(state, action, reward, next_state,win)
        self.observation = next_state
        self.learn()

        return action, win, cost, pos

def main():
    #def __init__(self,filename, input_dims, batch_size, gamma, epsilon, num_actions,
    # max_mem_size = 100000, eps_end=0.01, eps_dec=5e-4, discount = 1.0,learning_rate =0.7):
    dq = DQNAgent2("./puzzle_splited2.txt", gamma=0.99, epsilon=1.0, batch_size=64, n_actions=4,
                  input_dims=[6], lr=0.001)
    dq.run_puzzle(10)
if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()
