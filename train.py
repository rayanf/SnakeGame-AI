from game import snake_game
import pygame
from agent import Agent
pygame.init()


def train():
    plot_scores = []
    plot_mean_scores = []
    Tscore = 0
    record = 0
    agent = Agent()
    game = snake_game()
    game.reset()
    while True:
        before_state = agent.get_state(game)

        pygame_format_move, string_format_move = agent.get_action(before_state,game)

        reward, GameOver, score = game.one_step(pygame_format_move)

        after_state = agent.get_state(game)

        train_vector = [0,0,0]
        move_options = ['forward' ,'left' ,'right']
        train_vector[move_options.index(string_format_move)] = 1

        agent.train_short_memory(before_state, train_vector, reward, after_state, GameOver)

        agent.save_memory(before_state, pygame_format_move, reward, after_state, GameOver)

        if GameOver:
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game: ', agent.n_games, 'Score:', score, 'Record:', record)

            plot_scores.append(score)
            Tscore += score
            mean_score = Tscore / agent.n_games
            plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)
            game.reset()


if __name__ == '__main__':
    train()