import torch
import random
import numpy as np
from collections import deque
from game import snake_game
from model import Linear_QNet, QTrainer
import pygame
# from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(12, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake.rect.center
        point_l = (head[0] - 10, head[1])
        point_r = (head[0] + 10, head[1])
        point_u = (head[0], head[1] - 10)
        point_d = (head[0], head[1] + 10)

        dir_l = game.snake.direction == pygame.K_LEFT
        dir_r = game.snake.direction == pygame.K_RIGHT
        dir_u = game.snake.direction == pygame.K_UP
        dir_d = game.snake.direction == pygame.K_DOWN



        
         
        up_danger, right_danger, left_danger, down_danger = game.snake.get_danger()

        if up_danger and dir_u < 30:
            up_danger = 1
        else :
            up_danger = 0

        if down_danger and dir_d < 30:
            down_danger = 1
        else :
            down_danger = 0
        
        if right_danger and dir_r < 30:
            right_danger = 1
        else :
            right_danger = 0
            
        if left_danger and dir_l < 30:
            left_danger = 1
        else :
            left_danger = 0
        
        # try:
        state = [
            up_danger, right_danger, left_danger, down_danger,
            
            dir_l, dir_r, dir_u, dir_d,

            # Food location
            game.currentfood.rect.center[0] < game.snake.rect.center[0],  # currentfood left
            game.currentfood.rect.center[0] > game.snake.rect.center[0],  # currentfood right
            game.currentfood.rect.center[1] < game.snake.rect.center[1],  # currentfood up
            game.currentfood.rect.center[1] > game.snake.rect.center[1]  # currentfood down
        ]
        # except:
        #     state = [
        #         up_danger, right_danger, left_danger, down_danger,
                
        #         dir_l, dir_r, dir_u, dir_d,

        #         # Food location
        #         0,0,0,0 # currentfood down
        #     ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 50 - self.n_games
        final_move = [ pygame.K_RIGHT,pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            return final_move[move]
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            return final_move[move]



def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = snake_game()
    game.reset()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        reward, done, score = game.one_step(final_move)
        state_new = agent.get_state(game)
    
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)
            game.reset()


if __name__ == '__main__':
    train()