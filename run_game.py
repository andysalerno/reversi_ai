#!/usr/bin/env python3
from sys import argv
import time
from game.reversi import Reversi
from agents import random_agent, monte_carlo_agent, human_agent, q_learning_agent
from util import *
from prop_parse import prop_parse

prop_names = {
        # agent names. if user passes BlackAgent=human, becomes human_agent.Hu...
        'q_learning': q_learning_agent.QLearningAgent,
        'monte_carlo': monte_carlo_agent.MonteCarloAgent,
        'random': random_agent.RandomAgent,
        'human': human_agent.HumanAgent,
        }


def main(**kwargs):

    input_args = prop_parse(argv)
    input_args.update(kwargs)

    if len(argv) <= 1 and len(kwargs) <= 1:
        print('necessary inputs:')
        print('  BlackAgent=, WhiteAgent=,')
        print('    choices: q_learning, monte_carlo, random, human')
        print('optional inputs:')
        print('  size=(board size), amount=(#games), silent=(True/False)')
        quit()

    for k, v in input_args.items():
        # convert 'human' to human_agent.HumanAgent, etc
        if v in prop_names:
            input_args[k] = prop_names[v]
        # convert string 'True'/'False' to values
        elif v == 'True':
            input_args[k] = True
        elif v == 'False':
            input_args[k] = False
        elif v.isdigit():
            input_args[k] = int(v)
        else:
            print('unrecognized value {} for key {}.'.format(v, k))
            print('quitting.')
            quit()

    if any(val == monte_carlo_agent.MonteCarloAgent for val in input_args.values()) \
            and not input_args.get('time', False):
                print("Can't run monte carlo agent without passing in some value for time.")
                print('quitting.')
                quit()


    board_size = input_args.get('size', 8)
    amount = input_args.get('amount', 1)
    bot_time = input_args.get('bot_time', 1)
    set_output(input_args.get('silent', False))

    print('About to run {} games, black as {}, white as {}.'.format(
        amount, input_args['BlackAgent'], input_args['WhiteAgent'])
        )
    time.sleep(3)


    summary = []
    white_wins = 0
    black_wins = 0
    reversi = Reversi(board_size, **input_args)
    start = time.time()
    for t in range(1, amount + 1):
        info('starting game {} of {}'.format(t, amount))
        winner, white_score, black_score = reversi.play_game()
        if winner == WHITE:
            white_wins += 1
        elif winner == BLACK:
            black_wins += 1
        info('game {} complete.'.format(t))
        message = '{} wins! {}-{}'.format(
                color_name[winner], white_score, black_score)
        info(message)
        summary.append(message)
        reversi.reset()

    print('time: {} minutes'.format((time.time() - start) / 60))
    print('summary: {} games played'.format(len(summary)))
    for each in summary:
        info(each)
    print('Black won {}%'.format(black_wins / (black_wins + white_wins) * 100))
    print('White won {}%'.format(white_wins / (black_wins + white_wins) * 100))

    return (black_wins / (black_wins + white_wins)) * 100

if __name__ == '__main__':
    main()
