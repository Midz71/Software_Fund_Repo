# importing all the necessary modules for the entirety of the game
import random
import pygame
import copy
import sys
from pygame.locals import *

game_width = 7  # how wide the game will be
game_height = 6 # how high the game board will be
assert game_width >= 4 and game_height >= 4, 'Board must be at least 4x4.' # ensuring that the width and height of the game are in line with the rules of the game

user_name = input("What is your name? ") # asking the user for their name for later use
difficulty_selection = input("Please choose a number up to 2 for the difficulty.") # the user will decide what difficulty they want the game to be
computer_difficulty = int(difficulty_selection) # how many moves ahead the computer will think

counter_size = 50 # size of the tokens and individual board spaces in pixels

fps = 30 # frames per second to update the screen
user_window_width = 640 # width of the user's window, in pixels
user_window_height = 480 # height of the user's window in pixels

x_axis = int((user_window_width - game_width * counter_size) / 2) # defining the width of the game's x axis
y_axis = int((user_window_height - game_height * counter_size) / 2) # defining the height of the game's y axis

gold_colour = (212, 175, 55)
WHITE = (255, 255, 255)

background_colour = gold_colour # setting the colour of the game's background
text_colour = WHITE # setting the colour for the game text

RED = 'red'
BLACK = 'black'
EMPTY = None
HUMAN = user_name
COMPUTER = 'CPU'

def main(): #defining the main function for the game
    global FPSCLOCK, DISPLAYSURF, REDPILERECT, BLACKPILERECT, red_counter_pic
    global black_counter_pic, game_board_pic, ARROWIMG, ARROWRECT, user_win_pic
    global cpu_win_pic, WINNERRECT, draw_pic

    pygame.init() #begins to start up pygame module to create the game
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((user_window_width, user_window_height))
    pygame.display.set_caption('Welcome to Connect 4, ' + user_name +  "! \t Difficulty: " + difficulty_selection) # using the user's name and difficulty selection as a greeting & reminder in the window name
   
    REDPILERECT = pygame.Rect(int(counter_size / 2), user_window_height - int(3 * counter_size / 2), counter_size, counter_size)
    BLACKPILERECT = pygame.Rect(user_window_width - int(3 * counter_size / 2), user_window_height - int(3 * counter_size / 2), counter_size, counter_size)
    red_counter_pic = pygame.image.load('4row_red.png')
    red_counter_pic = pygame.transform.smoothscale(red_counter_pic, (counter_size, counter_size))
    black_counter_pic = pygame.image.load('4row_black.png')
    black_counter_pic = pygame.transform.smoothscale(black_counter_pic, (counter_size, counter_size))
    game_board_pic = pygame.image.load('4row_board.png')
    game_board_pic = pygame.transform.smoothscale(game_board_pic, (counter_size, counter_size))
    #importing the pictures to be used for the when the game is won by the user, won by the CPU or ends in a draw
    user_win_pic = pygame.image.load('4row_humanwinner.png')
    cpu_win_pic = pygame.image.load('4row_computerwinner.png')
    draw_pic = pygame.image.load('4row_tie.png')
    WINNERRECT = user_win_pic.get_rect()
    WINNERRECT.center = (int(user_window_width / 2), int(user_window_height / 2))

    ARROWIMG = pygame.image.load('4row_arrow.png')
    ARROWRECT = ARROWIMG.get_rect()
    ARROWRECT.left = REDPILERECT.right + 10
    ARROWRECT.centery = REDPILERECT.centery

    first_game = True

    while True: #checking that this is the user's first game and hasn't played this before
        runGame(first_game)
        first_game = False


def runGame(first_game):
    if first_game:
        # Let the computer go first on the first game, so the player
        # can see how the tokens are dragged from the token piles.
        game_turn = COMPUTER
        showHelp = True
    else:
        # Randomly choose who goes first.
        if random.randint(0, 1) == 0:
            game_turn = COMPUTER
        else:
            game_turn = HUMAN
        showHelp = False

    # Set up a blank board data structure.
    main_game_Board = getNewBoard()

    while True: # main game loop
        if game_turn == HUMAN:
            # the player's turn.
            getHumanMove(main_game_Board, showHelp)
            if showHelp:
                # turn off help arrow after the player's first move
                showHelp = False
            if isWinner(main_game_Board, RED): # a check to see if the user has won the game
                winner_pic = user_win_pic # if the user has won, display the picture to show so
                break
            game_turn = COMPUTER # switch to other player's turn
        else:
            # Computer's turn.
            column = getComputerMove(main_game_Board)
            animateComputerMoving(main_game_Board, column)
            make_move(main_game_Board, BLACK, column)
            if isWinner(main_game_Board, BLACK): # check if the CPU has won the game
                winner_pic = cpu_win_pic # if the CPU has won, display the picture to show so
                break
            game_turn = HUMAN # switch to the player's turn

        if isBoardFull(main_game_Board):
            # A completely filled board means it's a tie.
            winner_pic = draw_pic
            break

    while True:
        # Keep looping until player clicks the mouse or quits.
        drawBoard(main_game_Board)
        DISPLAYSURF.blit(winner_pic, WINNERRECT)
        pygame.display.update()
        FPSCLOCK.tick()
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return


def make_move(board, player, column):
    lowest = getLowestEmptySpace(board, column)
    if lowest != -1:
        board[column][lowest] = player


def drawBoard(board, extraToken=None):
    DISPLAYSURF.fill(background_colour)

    # draw tokens
    spaceRect = pygame.Rect(0, 0, counter_size, counter_size)
    for x in range(game_width):
        for y in range(game_height):
            spaceRect.topleft = (x_axis + (x * counter_size), y_axis + (y * counter_size))
            if board[x][y] == RED:
                DISPLAYSURF.blit(red_counter_pic, spaceRect)
            elif board[x][y] == BLACK:
                DISPLAYSURF.blit(black_counter_pic, spaceRect)

    # draw the extra token
    if extraToken != None:
        if extraToken['color'] == RED:
            DISPLAYSURF.blit(red_counter_pic, (extraToken['x'], extraToken['y'], counter_size, counter_size))
        elif extraToken['color'] == BLACK:
            DISPLAYSURF.blit(black_counter_pic, (extraToken['x'], extraToken['y'], counter_size, counter_size))

    # draw board over the tokens
    for x in range(game_width):
        for y in range(game_height):
            spaceRect.topleft = (x_axis + (x * counter_size), y_axis + (y * counter_size))
            DISPLAYSURF.blit(game_board_pic, spaceRect)

    # draw the red and black tokens off to the side
    DISPLAYSURF.blit(red_counter_pic, REDPILERECT) # red token on the left
    DISPLAYSURF.blit(black_counter_pic, BLACKPILERECT) # black token on the right


def getNewBoard():
    board = []
    for x in range(game_width):
        board.append([EMPTY] * game_height)
    return board


def getHumanMove(board, isFirstMove):
    draggingToken = False
    tokenx, tokeny = None, None
    while True:
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and not draggingToken and REDPILERECT.collidepoint(event.pos):
                # start of dragging on red token pile.
                draggingToken = True
                tokenx, tokeny = event.pos
            elif event.type == MOUSEMOTION and draggingToken:
                # update the position of the red token being dragged
                tokenx, tokeny = event.pos
            elif event.type == MOUSEBUTTONUP and draggingToken:
                # let go of the token being dragged
                if tokeny < y_axis and tokenx > x_axis and tokenx < user_window_width - x_axis:
                    # let go at the top of the screen.
                    column = int((tokenx - x_axis) / counter_size)
                    if isValidMove(board, column):
                        animateDroppingToken(board, column, RED)
                        board[column][getLowestEmptySpace(board, column)] = RED
                        drawBoard(board)
                        pygame.display.update()
                        return
                tokenx, tokeny = None, None
                draggingToken = False
        if tokenx != None and tokeny != None:
            drawBoard(board, {'x':tokenx - int(counter_size / 2), 'y':tokeny - int(counter_size / 2), 'color':RED})
        else:
            drawBoard(board)

        if isFirstMove:
            # Show the help arrow for the player's first move.
            DISPLAYSURF.blit(ARROWIMG, ARROWRECT)

        pygame.display.update()
        FPSCLOCK.tick()


def animateDroppingToken(board, column, color):
    x = x_axis + column * counter_size
    y = y_axis - counter_size
    dropSpeed = 2.0

    lowestEmptySpace = getLowestEmptySpace(board, column)

    while True:
        y += int(dropSpeed)
        dropSpeed += 0.5
        if int((y - y_axis) / counter_size) >= lowestEmptySpace:
            return
        drawBoard(board, {'x':x, 'y':y, 'color':color})
        pygame.display.update()
        FPSCLOCK.tick()


def animateComputerMoving(board, column):
    x = BLACKPILERECT.left
    y = BLACKPILERECT.top
    speed = 2.0
    # moving the black tile up
    while y > (y_axis - counter_size):
        y -= int(speed)
        speed += 0.5
        drawBoard(board, {'x':x, 'y':y, 'color':BLACK})
        pygame.display.update()
        FPSCLOCK.tick()
    # moving the black tile over
    y = y_axis - counter_size
    speed = 2.0
    while x > (x_axis + column * counter_size):
        x -= int(speed)
        speed += 0.5
        drawBoard(board, {'x':x, 'y':y, 'color':BLACK})
        pygame.display.update()
        FPSCLOCK.tick()
    # dropping the black tile
    animateDroppingToken(board, column, BLACK)


def getComputerMove(board):
    potentialMoves = getPotentialMoves(board, BLACK, computer_difficulty)
    # get the best fitness from the potential moves
    bestMoveFitness = -1
    for i in range(game_width):
        if potentialMoves[i] > bestMoveFitness and isValidMove(board, i):
            bestMoveFitness = potentialMoves[i]
    # find all potential moves that have this best fitness
    bestMoves = []
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveFitness and isValidMove(board, i):
            bestMoves.append(i)
    return random.choice(bestMoves)


def getPotentialMoves(board, tile, lookAhead):
    if lookAhead == 0 or isBoardFull(board):
        return [0] * game_width

    if tile == RED:
        enemyTile = BLACK
    else:
        enemyTile = RED

    # Figure out the best move to make.
    potentialMoves = [0] * game_width
    for firstMove in range(game_width):
        dupeBoard = copy.deepcopy(board)
        if not isValidMove(dupeBoard, firstMove):
            continue
        make_move(dupeBoard, tile, firstMove)
        if isWinner(dupeBoard, tile):
            # a winning move automatically gets a perfect fitness
            potentialMoves[firstMove] = 1
            break # don't bother calculating other moves
        else:
            # do other player's counter moves and determine best one
            if isBoardFull(dupeBoard):
                potentialMoves[firstMove] = 0
            else:
                for counterMove in range(game_width):
                    dupeBoard2 = copy.deepcopy(dupeBoard)
                    if not isValidMove(dupeBoard2, counterMove):
                        continue
                    make_move(dupeBoard2, enemyTile, counterMove)
                    if isWinner(dupeBoard2, enemyTile):
                        # a losing move automatically gets the worst fitness
                        potentialMoves[firstMove] = -1
                        break
                    else:
                        # do the recursive call to getPotentialMoves()
                        results = getPotentialMoves(dupeBoard2, tile, lookAhead - 1)
                        potentialMoves[firstMove] += (sum(results) / game_width) / game_width
    return potentialMoves


def getLowestEmptySpace(board, column):
    # Return the row number of the lowest empty row in the given column.
    for y in range(game_height-1, -1, -1):
        if board[column][y] == EMPTY:
            return y
    return -1


def isValidMove(board, column):
    # Returns True if there is an empty space in the given column.
    # Otherwise returns False.
    if column < 0 or column >= (game_width) or board[column][0] != EMPTY:
        return False
    return True


def isBoardFull(board):
    # Returns True if there are no empty spaces anywhere on the board.
    for x in range(game_width):
        for y in range(game_height):
            if board[x][y] == EMPTY:
                return False
    return True


def isWinner(board, tile):
    # check horizontal spaces
    for x in range(game_width - 3):
        for y in range(game_height):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True
    # check vertical spaces
    for x in range(game_width):
        for y in range(game_height - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                return True
    # check / diagonal spaces
    for x in range(game_width - 3):
        for y in range(3, game_height):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                return True
    # check \ diagonal spaces
    for x in range(game_width - 3):
        for y in range(game_height - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                return True
    return False


if __name__ == '__main__':
    main()