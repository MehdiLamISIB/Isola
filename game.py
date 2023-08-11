import pygame
import numpy as np
import minmax as minmax
# Initialize Pygame
pygame.init()

# Constants for board size and cell size
BOARD_SIZE = 7
CELL_SIZE = 80
SCREEN_SIZE = BOARD_SIZE * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK =(0,0,0)
# Create the screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Isola Game")

# Create the game board as a 2D numpy array
#board = np.zeros((BOARD_SIZE, BOARD_SIZE))
## variable global
FREE_CASE=0
JOUEUR_CASE=1
IA_CASE=2
WALL_CASE=-1
board=np.array( [
    [FREE_CASE,FREE_CASE,IA_CASE,FREE_CASE,FREE_CASE,FREE_CASE,FREE_CASE],
    [FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE],
    [FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE],
    [FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE],
    [FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE],
    [FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE],
    [FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, JOUEUR_CASE, FREE_CASE, FREE_CASE],
]
)



# Initial positions for player and AI
#player_position = (0, 2)
#ai_position = (6, 4)
#board[player_position] = 1
#board[ai_position] = 2

def move_player(move):
    global board

    # Get the current position of the player
    player_pos = np.array(np.where(board == JOUEUR_CASE))
    player_pos = [player_pos[0][0], player_pos[1][0]]

    # Calculate the new position after the move
    new_pos = [ move[0], move[1]]
    # Check if the new position is within the board boundaries
    if 0 <= new_pos[0] < 7 and 0 <= new_pos[1] < 7:
        if( (new_pos[0]-player_pos[0],new_pos[1]-player_pos[1]) in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]):
            # Check if the new position is a valid move (an empty cell)
            if board[new_pos[0]][new_pos[1]] == FREE_CASE:
                # Update the board with the new player position
                board[player_pos[0]][player_pos[1]] = FREE_CASE
                board[new_pos[0]][new_pos[1]] = JOUEUR_CASE
                # Toggle the current player
                return True  # Move was successful
    return False  # Move was invalid

def block_player(block):
    global board
    # Check if the clicked cell is a valid block position
    if board[block[0]][block[1]] == FREE_CASE:
        # Place the block in the clicked cell
        board[block[0]][block[1]] = WALL_CASE
        return True  # Block placement was successful
    return False  # Block placement was invalid


def Ia_turn():
    global board

    minmax.board_old=np.array(board)
    #root=minmax.Node(0)



    minmax.minmax(depth=0, alpha=float('-inf'), beta=float('inf'), maximizing_player=True,board=minmax.board_old)


    board=minmax.minmax_board

def check_winner(PLAYER_TYPE):
    pl_pos = np.array(np.where(board == PLAYER_TYPE)).reshape((2, 1))
    pl_pos = [pl_pos[1][0] , pl_pos[0][0] ]
    x=pl_pos[0]
    y=pl_pos[1]
    # ia_position = [x,y]
    loose_sum=0
    if(x==0 and y==0):
        return ( board[y+1][x]+ board[y+1][x+1]+ board[y][x+1]  )==-3
    elif (x == 6 and y == 0):
        return ( board[y+1][x]+ board[y+1][x+1]+ board[y][x+1]  )==-3
    elif (x == 0 and y == 6):
        return ( board[y-1][x]+board[y-1][x+1] + board[y][x+1]  )==-3
    elif (x == 6 and y == 6):
        return ( board[y-1][x-1]+board[y-1][x]+ + board[y][x-1] )==-3
    elif (x == 0):
        return ( board[y-1][x]+board[y-1][x+1] + board[y][x+1] + board[y+1][x]+ board[y+1][x+1] )==-5
    elif (x == 6):
        return ( board[y-1][x-1]+board[y-1][x] + board[y][x-1] + board[y+1][x-1]+ board[y+1][x] )==-5
    elif (y == 0):
        return ( board[y][x-1]+board[y][x+1] + board[y+1][x-1]+ board[y+1][x]+ board[y+1][x+1] )==-5
    elif (y == 6):
        return ( board[y-1][x-1]+board[y-1][x]+board[y-1][x+1] + board[y][x-1]+board[y][x+1]  )==-5
    else:
        return ( board[y-1][x-1]+board[y-1][x]+board[y-1][x+1] +
                 board[y][x-1]+board[y][x+1] +
                 board[y+1][x-1]+ board[y+1][x]+ board[y+1][x+1] )==-8






#GAME LOOP
#GAME LOOP
#GAME LOOP
#GAME LOOP
#GAME LOOP
#GAME LOOP
#GAME LOOP
#GAME LOOP
#GAME LOOP
#GAME LOOP

# Game loop

# Function to get the cell position based on the mouse click
def get_clicked_cell(mouse_pos):
    row = mouse_pos[1] // CELL_SIZE
    col = mouse_pos[0] // CELL_SIZE
    return row, col


running = True
clock = pygame.time.Clock()


## GAME STATUS
MOVE_PLAYER=1
BLOCK_PLAYER=1
IA_TURN=0
WINNER=0
while running:
    font = pygame.font.Font(None, 100)

    if(IA_TURN==1 ):
        minmax.board_old = np.array(board)
        minmax.minmax(depth=0, alpha=float('-inf'), beta=float('inf'), maximizing_player=True, board=minmax.board_old)
        board = minmax.minmax_board
        IA_TURN=0
        MOVE_PLAYER=1
        if(check_winner(JOUEUR_CASE)):
            WINNER=IA_CASE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
            clicked_row, clicked_col = get_clicked_cell(event.pos)
            print("Clicked on cell:", clicked_row, clicked_col)
            if(WINNER!=0):
                running=False
                break
            if(MOVE_PLAYER):
                if( move_player([int(clicked_row), int(clicked_col)]) ):
                    BLOCK_PLAYER=1
                    MOVE_PLAYER=0
                break
            if(BLOCK_PLAYER):
                if( block_player([int(clicked_row), int(clicked_col)]) ):
                    BLOCK_PLAYER=0
                    IA_TURN=1
                    if (check_winner(IA_CASE)):
                        WINNER = JOUEUR_CASE
                    break

            """
            C'est ici que pygame demarre une instance d'un tour Joueur-IA
            """





    screen.fill(WHITE)
    # Draw the board
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # le tableau est parcouru le long des x [---->]
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)  # Add this line to draw the grid
            cell_rect = pygame.Rect(x , y , CELL_SIZE, CELL_SIZE)
            #pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
            if board[row, col] == JOUEUR_CASE:  # Player
                pygame.draw.circle(screen, BLUE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 10)
            elif board[row, col] == IA_CASE:  # AI
                pygame.draw.circle(screen, RED, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 10)
            elif board[row, col] == WALL_CASE:

                pygame.draw.rect(screen, BLACK, cell_rect)

    #screen.blit(font.render("IA win !!", True, BLUE), (10, 240))
    if(WINNER==IA_CASE):
        screen.blit(font.render("IA win !!", True, BLUE), (10, 240))
    if(WINNER==JOUEUR_CASE):
        screen.blit(font.render("Joueur win !!", True, BLUE), (10, 240))
    pygame.display.flip()

    clock.tick(60)


pygame.quit()
