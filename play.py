from agent import Agent
from game import snake_game
import torch
from plot import plot


def play():

    plot_scores = []
    plot_mean_scores = []
    Tscore = 0
    record = 0
    agent = Agent()
    game = snake_game()
    game.reset()
    agent.model.load_state_dict(torch.load('./model/model.pth'))

    while True:
        before_state = agent.get_state(game)

        pygame_format_move, string_format_move = agent.play(before_state,game)

        reward, GameOver, score = game.one_step(pygame_format_move,before_state[8:])
        game.update_screen()
        game.clock.tick(game.fps)  
        


        if GameOver:
            agent.n_games += 1

            if score > record:
                record = score
                # agent.model.save()

            print('Game:', agent.n_games, 'Score:', score, 'Record:', record)

            plot_scores.append(score)
            Tscore += score
            mean_score = Tscore / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
            game.reset()


if __name__ == '__main__':
    play()