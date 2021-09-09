import torch
import random
import numpy as np
from collections import deque
from game import snake_game
from model import Linear_QNet, QTrainer
import pygame
from agent import Agent
# from helper import plot
pygame.init()


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = snake_game()
    game.reset()
    while True:
        state_old = agent.get_state(game)

        final_move, train_move = agent.get_action(state_old,game)

        reward, done, score = game.one_step(final_move)
        state_new = agent.get_state(game)

        train_moves = [0,0,0]
        move_options = ['forward' ,'left' ,'right']
        train_moves[move_options.index(train_move)] = 1
        agent.train_short_memory(state_old, train_moves, reward, state_new, done)

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