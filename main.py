from Training import Training
from Window import Window
from UI.Menu import Menu

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Learn2Slither',
                                     description='Teach an AI to play\
                                          Snake using Q-learning')
    parser.add_argument('-sessions', type=int, default=1000,
                        help='Number of sessions to run (default = 1000).\
                            0 or a negative number will skip training.')
    parser.add_argument('-size', type=int, default=10,
                        help='Size of the grid (default = 10, min = 5)')
    parser.add_argument('-save', type=str, help='File to save the model to')
    parser.add_argument('-choosetosave', action='store_true',
                        help='Choose whether to save the model or not after it\
                            finished training (default = off)')
    parser.add_argument('-load', type=str, help='File to load the model from')
    parser.add_argument('-dontlearn', action='store_true',
                        help='Don\'t update the Q-table')
    parser.add_argument('-visual', action='store_true',
                        help='Enable visual mode (default = off)')
    parser.add_argument('-speed', type=int, default=10,
                        help='Speed the game is displayed at (default = 10),\
                            only used in visual mode.')
    parser.add_argument('-plot', action='store_true', help='Plot the results')
    parser.add_argument('-ui', action='store_true',
                        help='Enable the user interface (default = off).\
                            Any other arg will not be considered')
    parser.add_argument('-stepbystep', action='store_true',
                        help='Shows each move step by step in visual mode')
    parser.add_argument('-nerd', action='store_true',
                        help='Show stats for nerd (default = off),\
                            only used in visual mode')

    args = parser.parse_args()

    if args.ui:
        ui = Menu()
        ui.run()

    else:
        training = Training(args)
        training.train()

        if args.visual:
            if args.size < 101:
                w = Window(training)
                w.run()
            else:
                print("\033[91m\033[1mEXCEPTION RAISED: Can't open a window if\
    the grid size is more than 100. Skipped.\033[0m")
