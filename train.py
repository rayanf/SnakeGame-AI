from game import snake_game
import pygame
from agent import Agent
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
        before_state = agent.get_state(game)

        final_move, train_move = agent.get_action(before_state,game)

        reward, GameOver, score = game.one_step(final_move)

        after_state = agent.get_state(game)

        train_moves = [0,0,0]
        move_options = ['forward' ,'left' ,'right']
        train_moves[move_options.index(train_move)] = 1

        agent.train_short_memory(before_state, train_moves, reward, after_state, GameOver)

        agent.save_memory(before_state, final_move, reward, after_state, GameOver)

        if GameOver:
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