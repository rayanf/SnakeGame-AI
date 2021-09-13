import torch
import random
import numpy as np
from collections import deque
from game import snake_game
from model_torch import Linear_QNet, QTrainer
import pygame
# from game import check_lock

pygame.init()
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 
        self.gamma = 0.96
        self.memory = deque(maxlen=MAX_MEMORY) 
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        l_direction = game.snake.direction == pygame.K_LEFT
        r_direction = game.snake.direction == pygame.K_RIGHT
        u_direction = game.snake.direction == pygame.K_UP
        d_direction = game.snake.direction == pygame.K_DOWN

        up_danger, right_danger, left_danger, down_danger = game.snake.get_danger()

        if up_danger <= 20:
            up_danger = 1
        else :
            up_danger = 0

        if down_danger <= 20 :
            down_danger = 1
        else :
            down_danger = 0
        
        if right_danger <= 20:
            right_danger = 1
        else :
            right_danger = 0
            
        if left_danger <= 20 :
            left_danger = 1
        else :
            left_danger = 0

        forward_danger, left_danger, right_danger = self.absolute_to_relative(game.snake.direction, [up_danger, right_danger, down_danger, left_danger,])
        forward_path,left_path,right_path = game.check_path()

        if 1 not in  (forward_path,left_path,right_path):
            forward_path,left_path,right_path = forward_danger, left_danger, right_danger
            print('change feature')

        state = [
            # forward_danger,
            # left_danger,
            # right_danger,
            
            l_direction,
            r_direction,
            u_direction,
            d_direction,

            game.currentfood.rect.center[0] < game.snake.rect.center[0],  
            game.currentfood.rect.center[0] > game.snake.rect.center[0],  
            game.currentfood.rect.center[1] < game.snake.rect.center[1],  
            game.currentfood.rect.center[1] > game.snake.rect.center[1],

            forward_path,
            left_path,
            right_path
            
        ]
    
        return np.array(state, dtype=int)

    def save_memory(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) 
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, game):
        self.epsilon = 200 - self.n_games
        final_move = ['forward' ,'left' ,'right']
        if random.randint(0, 400) < self.epsilon:
            move = random.randint(0, 2)
            return self.relativ_to_absolute(final_move[move],game.snake.direction),final_move[move]
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            return  self.relativ_to_absolute(final_move[move],game.snake.direction),final_move[move]


    def relativ_to_absolute(self,relativeDirect,curent_ABSdirection):
        relativD = {'forward':0,'left':1,'right':-1}
        pygame_format_ABSdirection = [pygame.K_UP,pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]
        curent_ABSdirection_Index = pygame_format_ABSdirection.index(curent_ABSdirection)
        ABS_direction = pygame_format_ABSdirection[(curent_ABSdirection_Index - relativD[relativeDirect])%4]
        return ABS_direction

    def absolute_to_relative(self,curentDirect,Directions):
        direction_Index = {pygame.K_UP : 0 ,pygame.K_RIGHT : 1 ,pygame.K_DOWN : 2 ,pygame.K_LEFT : 3 }
        return (Directions[(direction_Index[curentDirect]%4)], Directions[(direction_Index[curentDirect]-1)%4], Directions[(direction_Index[curentDirect]+1)%4])
