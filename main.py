import numpy as np
from random import randrange
import minmax as minmax
"""
Le déroulement du jeu se passe ainsi :
    - D'abord le joueur bouge et pose un block
    - Ensuite le joueur IA prend la meilleur option (minmax) et pose un block
"""

"""
Valeur heuristique
    - Distance par rapport à l'opposant : distance Manhattan
    - Controle du centre du plateau : Valeur élévé pour les case proche du centre du plateau
    - Isolation de l'opposant : Positif si une case près de l'opposant est bloqué
    - 
"""

## variable global
FREE_CASE=0
JOUEUR_CASE=1
IA_CASE=2
WALL_CASE=-1



WINNER_GAME=0

board= np.array( [
    [FREE_CASE,FREE_CASE,IA_CASE,FREE_CASE,FREE_CASE,FREE_CASE,FREE_CASE],
    [FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE],
    [FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE],
    [FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE],
    [FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE],
    [FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE],
    [FREE_CASE, FREE_CASE, FREE_CASE, FREE_CASE, JOUEUR_CASE, FREE_CASE, FREE_CASE],
]
)











def show_board():
    global board
    print(" ",end="")
    print("-"*21)
    for a in board:
        for i in a:
            print("{}".format(i).rjust(3), end="")
        print(end="\n")
    print(" ", end="")
    print("-" * 21)
def move_player():
    position_accepted = False
    print("******************************")
    print("| Phase choix de la position |")
    print("******************************")
    while(not position_accepted):
        # permet de transformer [[1],[1]] en [1,2]
        player_pos = np.array(np.where(board == JOUEUR_CASE)).reshape((2, 1))
        player_pos=[player_pos[0][0]+1,player_pos[1][0]+1]
        print("Votre position actuelle ({1},{0})".format(player_pos[0],player_pos[1]))
        move_choose = str(input("choix x,y --> "))
        coord = list(move_choose.split(','))
        # pour la position on doit :
        # - verifier si entier
        # - verifier si position même que avant
        # - verifier si position autour
        # - a la fin verifier si prochaine position est un mur ou IA, pour éviter des soucis
        if(coord[0].isdigit() and coord[1].isdigit()):
            coord=[int(coord[1]),int(coord[0])]
            if(coord[0]>7 or coord[0]<1):
                print("Case x en dehors du plateau !!!!")
                continue
            if(coord[1]>7 or coord[1]<1):
                print("Case y en dehors du plateau !!!!")
                continue
            print("cooord ---> ",coord)
            print("player_pos --->", player_pos)
            if(
                    (not (coord[0]==player_pos[0] and coord[1]==player_pos[1] ) )
                and (
                    (coord[0] == (player_pos[0] - 1) or coord[0] == (player_pos[0] + 1) or coord[0]==player_pos[0] )
                        or
                    (coord[1] == (player_pos[1] - 1) or coord[1] == (player_pos[1] + 1) or coord[1]==player_pos[1] )
                    )
            ):

                if(board[coord[0]-1][coord[1]-1]==IA_CASE or board[coord[0]-1][coord[1]-1]==WALL_CASE):
                    print("Position occupé !!!!!")
                    continue
                board[coord[0]-1][coord[1]-1]=JOUEUR_CASE
                board[player_pos[0]-1][player_pos[1]-1]=FREE_CASE
                position_accepted=True
                continue
            else:
                print("Choisi les bonnes cases !!!!")
                continue

        else:
            print("Mets des chiffres !!!!!!")
            continue
    ## position choisi maintenat on peut poser le mur
def block_player():
    position_accepted = False
    print("******************************")
    print("| Phase choix position du mur |")
    print("******************************")
    while(not position_accepted):
        # permet de transformer [[1],[1]] en [1,2]
        player_pos = np.array(np.where(board == JOUEUR_CASE)).reshape((2, 1))
        player_pos=[player_pos[0][0]+1,player_pos[1][0]+1]
        print("Votre position actuelle ({1},{0})".format(player_pos[0],player_pos[1]))
        move_choose = str(input("choix x,y --> "))
        coord = list(move_choose.split(','))
        # pour la position on doit :
        # - verifier si entier
        # - verifier si prochaine position est un mur ou IA, pour éviter des soucis
        if(coord[0].isdigit() and coord[1].isdigit()):
            coord=[int(coord[1]),int(coord[0])]
            print("cooord ---> ",coord)
            print("player_pos --->", player_pos)

            if(coord[0]>7 or coord[0]<1):
                print("Case x en dehors du plateau !!!!")
                continue
            if(coord[1]>7 or coord[1]<1):
                print("Case y en dehors du plateau !!!!")
                continue

            if(board[coord[0]-1][coord[1]-1]==FREE_CASE):
                board[coord[0]-1][coord[1]-1]=WALL_CASE
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





#A faire
def Ia_turn():
    minmax.board=board
    root=minmax.Node(0)
    print(minmax.minmax(root, depth=2, alpha=float('-inf'), beta=float('inf'), maximizing_player=True))


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


def isola_game():
    global board,WINNER_GAME
    while(True):
        ## D'abord je montre le plateau
        show_board()
        # Ensuite le joueur doit choisir les cases et poser le mur
        Player_turn()
        # Ensuite une évaluation des condition de réussite sont faite

        if(check_winner(IA_CASE)):
            print("\n"*10)
            print("Bien joué, tu as gagné contre l'IA")
            WINNER_GAME=JOUEUR_CASE
            break
        # Ensuite le joueur IA doit choisir les cases et poser le mur
        Ia_turn()
        # Ensuite une évaluation des condition de réussite sont faite
        if(check_winner(JOUEUR_CASE)):
            print("\n"*10)
            print("Tu as perdu contre l'IA")
            WINNER_GAME=IA_CASE
            break

#show_board()

isola_game()




#empty_cells=np.array(np.where(board == FREE_CASE))
#empty_cells=[ [empty_cells[0][i],empty_cells[1][i]] for i in range(len(empty_cells[0]))]
#print(empty_cells)