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
WINNER_GAME=0
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

def block_player():
    position_accepted = False
    print("******************************",end='')
    print("| Phase choix position du mur |",end='')
    print("******************************")
    while(not position_accepted):
        # permet de transformer [[1],[1]] en [1,2]
        player_pos = np.array(np.where(board == JOUEUR_CASE)).reshape((2, 1))
        player_pos=[player_pos[0][0],player_pos[1][0]]
        print("Votre position actuelle ({0},{1}) ---- ".format(player_pos[0],player_pos[1]),end='')
        move_choose = str(input("choix y,x --> "))
        coord = list(move_choose.split(','))
        # pour la position on doit :
        # - verifier si entier
        # - verifier si prochaine position est un mur ou IA, pour éviter des soucis
        if(coord[0].isdigit() and coord[1].isdigit()):
            coord=[int(coord[0]),int(coord[1])]
            #print("cooord ---> ",coord)
            #print("player_pos --->", player_pos)

            if(coord[0]>7 or coord[0]<0):
                print("Case x en dehors du plateau !!!!")
                continue
            if(coord[1]>7 or coord[1]<0):
                print("Case y en dehors du plateau !!!!")
                continue
            if(board[coord[0]][coord[1]]==FREE_CASE):
                board[coord[0]][coord[1]]=WALL_CASE
                position_accepted=True
                continue
            else:
                print("Position occupé !!!!")
                continue
        else:
            print("Mets des chiffres !!!!!!")

    ## position choisi maintenat on peut poser le mur

def Player_turn():
    move_player()
    block_player()

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



MOVE_PLAYER=1
BLOCK_PLAYER=1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
            clicked_row, clicked_col = get_clicked_cell(event.pos)
            print("Clicked on cell:", clicked_row, clicked_col)
            print("peut bouger", move_player([int(clicked_row), int(clicked_col)]))


            #if(MOVE_PLAYER):
            #    BLOCK_PLAYER=1
            #    MOVE_PLAYER=0
            #    print("MOVE")
            #    break
            #if(BLOCK_PLAYER):
            #    print("BLOCk")
            #    BLOCK_PLAYER=0
            #    break

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
            #pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
            if board[row, col] == JOUEUR_CASE:  # Player
                pygame.draw.circle(screen, BLUE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 10)
            elif board[row, col] == IA_CASE:  # AI
                pygame.draw.circle(screen, RED, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 10)

    pygame.display.flip()


    clock.tick(60)


pygame.quit()
