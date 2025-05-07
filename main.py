from Training import Training
from Window import Window

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Learn2Slither',
                                     description='Teach an AI to play\
                                          Snake using Q-learning')
    parser.add_argument('-sessions', type=int, default=1000,
                        help='Number of sessions to run (default = 1000)')
    parser.add_argument('-size', type=int, default=10,
                        help='Size of the grid (default = 10, min = 5)')
    parser.add_argument('-save', type=str, help='File to save the model to')
    parser.add_argument('-choosetosave', action='store_true',
                        help='Choose whether to save the model or not')
    parser.add_argument('-load', type=str, help='File to load the model from')
    parser.add_argument('-dontlearn', action='store_true',
                        help='Don\'t update the Q-table')
    parser.add_argument('-visual', action='store_true',
                        help='Enable or disable visual mode (default = off)')
    parser.add_argument('-plot', action='store_true', help='Plot the results')
    parser.add_argument('-ui', action='store_true',
                        help='Enable the user interface')
    parser.add_argument('-stepbystep', action='store_true',
                        help='Shows each move step by step in visual mode')
    parser.add_argument('-nerd', action='store_true',
                        help='Show stats for nerd (default = off)')

    args = parser.parse_args()
    print(args)

    training = Training(args)
    training.train()

    if args.visual:
        w = Window(training)
        w.run()
