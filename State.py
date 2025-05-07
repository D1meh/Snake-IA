from Game import Game


class State:
    def __init__(self, game: Game):
        self.game = game

    # 	# Debug
    # 	self.startingPos = game.snake.getHead()
    # 	self.history = []
    # 	self.count = 0

    # def addHistory(self, direction):
    # 	self.history.append(direction)
    # 	self.count += 1

    # Private

    def __checkCell(self, x, y, cellType):
        board = self.game.board
        try:
            return board[y][x] in cellType
        except IndexError:
            if cellType == 'WS':
                return True
            return False

    def __checkDanger(self):
        snakeX, snakeY = self.game.snake.getHead()

        return (
            self.__checkCell(snakeX, snakeY - 1, 'WS'),
            self.__checkCell(snakeX, snakeY + 1, 'WS'),
            self.__checkCell(snakeX - 1, snakeY, 'WS'),
            self.__checkCell(snakeX + 1, snakeY, 'WS')
        )

    def __checkRed(self):
        snakeX, snakeY = self.game.snake.getHead()

        return (
            self.__checkCell(snakeX, snakeY - 1, 'R'),
            self.__checkCell(snakeX, snakeY + 1, 'R'),
            self.__checkCell(snakeX - 1, snakeY, 'R'),
            self.__checkCell(snakeX + 1, snakeY, 'R')
        )

    def __checkGreen(self):
        snakeX, snakeY = self.game.snake.getHead()

        checkNorth = snakeY - 1
        checkSouth = snakeY + 1
        checkEast = snakeX + 1
        checkWest = snakeX - 1
        while self.__checkCell(snakeX, checkNorth, '0'):
            checkNorth -= 1
        while self.__checkCell(snakeX, checkSouth, '0'):
            checkSouth += 1
        while self.__checkCell(checkEast, snakeY, '0'):
            checkEast += 1
        while self.__checkCell(checkWest, snakeY, '0'):
            checkWest -= 1

        return (
            self.__checkCell(snakeX, checkNorth, 'G'),
            self.__checkCell(snakeX, checkSouth, 'G'),
            self.__checkCell(checkEast, snakeY, 'G'),
            self.__checkCell(checkWest, snakeY, 'G')
        )

    # Public

    def __checkIfDead(self):
        snakeX, snakeY = self.game.snake.getHead()
        return self.__checkCell(snakeX, snakeY, 'WS')

    def getState(self):
        if self.__checkIfDead():
            return ("DEAD", "DEAD", "DEAD")
        
        return (self.__checkDanger(), self.__checkRed(), self.__checkGreen())
