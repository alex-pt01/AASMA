import math
import numpy as np
  
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

import tensorflow as tf


"""
Must modify code so that:
1 - States and Observations be txt from the puzzles and not float32


"""

class DeepQNetwork(nn.Module):
    def __init__(self, input_dims, lr, fc1_dims, fc2_dims, num_actions):
        super(DeepQNetwork, self).__ini__()
        self.learning_rate = lr
        self.input_dims = input_dims
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.num_actions = num_actions
        self.fc1 = nn.Linear(*self.input_dims, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc2_dims, self.fc2_dims)
        self.fc3 = nn.Linear(self.fc2_dims, self.num_actions)
        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.loss = nn.MSELoss()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(self.device)
    
    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        actions = self.fc3(x)
        return actions 

        
class DQNAgent():
    def __init__(self,filename, input_dims, batch_size, gamma, epsilon, num_actions,
    max_mem_size = 100000, eps_end=0.01, eps_dec=5e-4, discount = 1.0,learning_rate =0.7):
        self.filename = filename
        self.discount = discount
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_min = eps_end
        self.eps_dec = eps_dec
        self.action_space = [i for i in range(num_actions)]
        self.mem_size = max_mem_size
        self.batch_size = batch_size
        self.mem_cntr = 0

        self.Q_eval = DeepQNetwork(self.learning_rate, num_actions=4, input_dims=input_dims, fc1_dims=256, fc2_dims=256)

        self.state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32) #FIXME
        self.new_state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32) #FIXME

        self.action_memory = np.zeros(self.mem_size,  dtype=np.float32)
        self.reward_memory = np.zeros(self.mem_size,  dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size,  dtype=np.bool)

    def store_transition(self, state, action, reward, next_state, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = next_state
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.terminal_memory[index] = done

        self.mem_cntr +=1
    
    def choose_action(self, observation):
        if np.random() > self.epsilon:
            state = T.tensor([observation]).to(self.Q_eval.device)
            actions = self.Q_eval.forward(state)
            action = T.argmax(actions).item()
        else:
            action = np.random.choice(self.action_space)
        return action

    def learn(self):
        if self.mem_cntr < self.batch_size:
            return
        
        self.Q_eval.optimizer.zero_grad()

        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, self.batch_size, replace = False)

        batch_index = np.arange(self.batch_size, dtype=np.int32)

        state_batch = T.tensor(self.state_memory[batch]).to(self.Q_eval.device)
        new_state_batch = T.tensor(self.new_state_memory[batch]).to(self.Q_eval.device)
        reward_batch = T.tensor(self.reward_memory[batch]).to(self.Q_eval.device)
        terminal_batch = T.tensor(self.terminal_memory[batch]).to(self.Q_eval.device)
        action_batch = self.action[batch]

        q_eval = self.Q_eval.forward(state_batch)[batch_index, action_batch]
        q_next = self.Q_eval.forward(new_state_batch)
        q_next[terminal_batch] = 0.0

        q_target = reward_batch + self.gamma * T.max(q_next, dim=1)[0]

        loss = self.Q_eval.loss(q_target, q_eval).to(self.Q_eval.device)
        loss.backward()
        self.Q_eval.optimizer.step()

        if(self.epsilon>self.eps_min):
            self.epsilon-= self.eps_dec
        else:
            self.epsilon = self.eps_min




