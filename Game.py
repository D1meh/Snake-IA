from random import randint


class Snake:
    def __init__(self):
        self.size = 3
        self.pos = []

    def move(self, direction):
        x, y = self.pos[0]
        if direction == 'U':
            self.pos.insert(0, (x, y - 1))
        elif direction == 'D':
            self.pos.insert(0, (x, y + 1))
        elif direction == 'L':
            self.pos.insert(0, (x - 1, y))
        elif direction == 'R':
            self.pos.insert(0, (x + 1, y))

        self.pos.pop()

    def grow(self, lastPosition):
        self.pos.append(lastPosition)
        self.size += 1

    def shrink(self):
        self.pos.pop()
        self.size -= 1

    def getHead(self):
        return self.pos[0]


class Game:
    def __init__(self, size=10, printDeath=False):
        self.size = size
        self.board = [['W' if i == 0 or i == size+1 or j == 0 or j == size+1
                       else '0' for i in range(size+2)] for j in range(size+2)]
        self.greenApples = []
        self.redApple = []
        self.gameOver = False

        self.snake = Snake()
        self.generateStartingPosition()

        self.generateGreenApple()
        self.generateGreenApple()
        self.generateRedApple()

        self.printDeath = printDeath

    def generateStartingPosition(self):
        x, y = randint(1, self.size), randint(1, self.size)
        self.snake.pos.append((x, y))
        self.board[y][x] = 'H'

        lastX, lastY = x, y
        numberOfSegments = self.snake.size - 1
        while True:

            if numberOfSegments == 0:
                break

            direction = randint(0, 3)
            if direction == 0:
                x, y = lastX, lastY - 1
            elif direction == 1:
                x, y = lastX, lastY + 1
            elif direction == 2:
                x, y = lastX - 1, lastY
            else:
                x, y = lastX + 1, lastY

            if x >= 0 and x <= self.size and y >= 0 \
                    and y <= self.size and self.board[y][x] == '0':
                self.snake.pos.append((x, y))
                self.board[y][x] = 'S'
                lastX, lastY = x, y
                numberOfSegments -= 1

    def generateApple(self):
        x, y = randint(1, self.size), randint(1, self.size)
        return x, y

    def generateGreenApple(self):
        while True:
            x, y = self.generateApple()
            if self.board[y][x] == '0':
                break

        self.greenApples.append((x, y))
        self.board[y][x] = 'G'

    def generateRedApple(self):
        while True:
            x, y = self.generateApple()
            if self.board[y][x] == '0':
                break

        self.redApple = [(x, y)]
        self.board[y][x] = 'R'

    def update(self, direction):
        currentCell = None

        currentSnakePositions = self.snake.pos.copy()
        for i in range(len(currentSnakePositions)):
            x, y = currentSnakePositions[i]
            self.board[y][x] = '0'

        self.snake.move(direction)
        snakePositions = self.snake.pos

        shouldGenerateGreen, shouldGenerateRed = False, False
        for i in range(len(snakePositions)):

            if i == len(snakePositions):  # happens after eating a red apple
                break

            x, y = snakePositions[i]
            if currentCell is None:
                currentCell = self.board[y][x]

            if self.board[y][x] == 'G':
                shouldGenerateGreen = True
                lastPosition = currentSnakePositions[-1]
                self.snake.grow(lastPosition)
                self.board[lastPosition[1]][lastPosition[0]] = 'S'
            elif self.board[y][x] == 'R':
                shouldGenerateRed = True
                self.snake.shrink()
                if self.snake.size == 0:
                    self.gameOver = True
                    if self.printDeath:
                        print("Red apple", direction)
            elif self.board[y][x] == 'W' or\
                    ((x, y) in currentSnakePositions and i == 0):
                self.gameOver = True
                if self.printDeath:
                    print("Wall" if self.board[y][x] == 'W' else "Snake", direction)

            self.board[y][x] = 'H' if i == 0 else 'S'

        if shouldGenerateGreen:
            self.generateGreenApple()
        if shouldGenerateRed:
            self.generateRedApple()

        return currentCell
