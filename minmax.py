import numpy as np
import random as rd
FREE_CASE=0
JOUEUR_CASE=1
IA_CASE=2
WALL_CASE=-1

DEPTH_MAX=2

board_old=[]
minmax_board=[]





class Node():
    def __init__(self, value):
        # Heurestic value
        self.value = value
        self.child_nodes=[]
        self.child_count=0
        self.board=[]
    def AddNode(self,node):

        self.child_nodes.append(node)
        self.child_count=len(self.child_nodes)

### Fonction peut être utiliser pour Joueur et IA
def check_block_around(board,PLAYER_TYPE):
    pl_pos = np.array(np.where(board == PLAYER_TYPE))
    pl_pos = [pl_pos[1][0] , pl_pos[0][0] ]
    x=pl_pos[0]
    y=pl_pos[1]
    # ia_position = [x,y]
    loose_sum=0
    if(x==0 and y==0):
        #Max -3
        return abs(board[y+1][x]+ board[y+1][x+1]+ board[y][x+1])
    elif (x == 6 and y == 0):
        return abs( board[y+1][x]+ board[y+1][x-1]+ board[y][x-1]  )
    elif (x == 0 and y == 6):
        return abs( board[y-1][x]+board[y-1][x+1] + board[y][x+1]  )
    elif (x == 6 and y == 6):
        return abs( board[y-1][x-1]+board[y-1][x]+ + board[y][x-1] )
    elif (x == 0):
        #Max -5
        return abs( board[y-1][x]+board[y-1][x+1] + board[y][x+1] + board[y+1][x]+ board[y+1][x+1] )
    elif (x == 6):
        return abs( board[y-1][x-1]+board[y-1][x] + board[y][x-1] + board[y+1][x-1]+ board[y+1][x] )
    elif (y == 0):
        return abs( board[y][x-1]+board[y][x+1] + board[y+1][x-1]+ board[y+1][x]+ board[y+1][x+1] )
    elif (y == 6):
        return abs( board[y-1][x-1]+board[y-1][x]+board[y-1][x+1] + board[y][x-1]+board[y][x+1]  )
    else:
        #max 8, si 8 alors joueur PERDU !!!!!
        return abs( board[y-1][x-1]+board[y-1][x]+board[y-1][x+1] +
                 board[y][x-1]+board[y][x+1] +
                 board[y+1][x-1]+ board[y+1][x]+ board[y+1][x+1] )

def check_move_around(board,PLAYER_TYPE):
    moves = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    pl_pos = np.array(np.where(board == PLAYER_TYPE))
    pl_pos = [pl_pos[0][0], pl_pos[1][0]]
    count_move=0
    for pos in directions:
        x = pos[1]
        y = pos[0]
        if ( (pl_pos[1] + x < 0) or (pl_pos[1] + x > 6) or (pl_pos[0] + y < 0) or (pl_pos[0] + y > 6) ):
            continue
        if(board[pl_pos[0] + y][pl_pos[1] + x]!=FREE_CASE):
            continue
        count_move=count_move+1
    return count_move

def make_move(board,move,PLAYER_TYPE):
    move_board = np.array(board)#np.array( np.where(board == PLAYER_TYPE, FREE_CASE, board) )
    old_position=np.array(np.where(board==PLAYER_TYPE))
    move_board[old_position[0][0],old_position[1][0]]=FREE_CASE
    move_board[move[0], move[1]] = PLAYER_TYPE
    return move_board

def place_block(board,block):
    # ajoute le block
    block_board=np.array(board)
    block_board[block[0], block[1]] = WALL_CASE
    return block_board

def generate_moves_and_blocks(board, PLAYER_TYPE):
    moves = []
    blocks = []
    # Les directions que peut faire l'IA ou le joueur
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    pl_pos = np.array(np.where(board == PLAYER_TYPE))
    pl_pos = [pl_pos[0][0], pl_pos[1][0]]
    # On verifie si ces mouvements sont possibles, si oui on les rajoutes dans la listes des mouvements
    # ici pour moves --> on a les coordonnées qui commence par 0 (0,0) est donc la position du corner supérieur gauche |
    for pos in directions:
        x = pos[1]
        y = pos[0]
        if ( (pl_pos[1] + x < 0) or (pl_pos[1] + x > 6) or (pl_pos[0] + y < 0) or (pl_pos[0] + y > 6) ):
            continue
        if(board[pl_pos[0] + y][pl_pos[1] + x]!=FREE_CASE):
            continue
        moves.append([pl_pos[0] + y, pl_pos[1] + x])
        # Pour optimiser, et eviter de reutiliser 2 fois la même boucle,
        # je vérifie le mouvement et attribue la liste des endroit qui peuvent être bloqué
        move_board = make_move(board, [pl_pos[0] + y, pl_pos[1] + x], PLAYER_TYPE)
        empty_cells = np.array(np.where(move_board == FREE_CASE)).T

        blocks.append(empty_cells.tolist())
    """
    Pour chaque move, on aura un block associe
    
    moves -- comprend les positions que le joueur/IA peut faire
    blocks -- tableau qui comprend le tableau avec chaque position bloque , ce tableau est liés au mouvement du joueur
    [ [(0,1),(3,2)],.... ]
    |   ^
    |   |
    |   tableau qui présente les endroit libre pour bloque lies au mouvement fait dans le même tour (car 2 choix a faire dans un même tour)
    |---|
    """
    return moves, blocks

"""
Liste des variables heuristiques:
    LIES AU JOUEUR (poids positif):
    - p1: position du joueur
    - p2: distance au joueur
    - p3: nombre de bloc autour du joueur
    
    LIES A l'IA (poids negatif):
    - n1: distance par rapport au coin
    - n2: nombre de bloc autour de l'IA
    
    Je dois aussi prendre en compte la séquence :
    - D'abord l'IA bouge puis pose son bloc
    
    Donc une valeur heuristique pour le mouvement et une pour poser le bloc
"""

def evaluate_board(board,PLAYER_TYPE):
    """
    Test fonction d'evaluation
    --> on essaie d'entourer l'adversaire le plus rapidement
    --> on privilegie les mouvement au centre
    --> on
    """
    player_pos = np.where(board == PLAYER_TYPE)
    player_pos = [player_pos[0][0], player_pos[1][0]]
    manthann_distance=abs(3-player_pos[0])+abs(3-player_pos[1])

    if(PLAYER_TYPE==IA_CASE):
        # retourne le nombre de case autour du joueur
        block_adversary = check_block_around(board,JOUEUR_CASE)
        move_adversary=check_move_around(board,JOUEUR_CASE)
        block_player = check_block_around(board,IA_CASE)
        move_player=check_move_around(board,IA_CASE)
    else:
        block_adversary = check_block_around(board,IA_CASE)
        move_adversary=check_move_around(board,IA_CASE)
        block_player = check_block_around(board,JOUEUR_CASE)
        move_player = check_move_around(board, JOUEUR_CASE)

    # On veut :
    # Maximiser
    # --> les blocs autour de l'adversaire
    # --> l'espace libre
    # Minimiser
    # --> les blocs autour du joueur
    # --> les mouvements vers les coins
    # --> les mouvements de l'adversaire


    return 10*(block_adversary+move_player)-(manthann_distance+block_player+move_adversary)


def minmax(depth, alpha, beta, maximizing_player,board):
    global minmax_board
    """
    :param node: noeud racine
    :param depth: profondeur
    :param alpha: meilleur maximimum
    :param beta: meilleur minimum
    :param maximizing_player: est ce qu'on maximise ?
    :return:
    """
    ## permet de sauvegarder le meilleur tableau possible, évite de dépendre de ma classe Node !!!
    best_board=np.array(board)
    ### Cas 1: Profondeur==0 --> recursion finale, retour de la pile
    if(depth == DEPTH_MAX):
        value=0
        if(maximizing_player):
            value=evaluate_board(np.array(board),IA_CASE)
        else:
            value=evaluate_board(np.array(board),JOUEUR_CASE)
        return value
    elif(maximizing_player):
        """
        L'algoritme itere tous les cas possible
        pour maximiser l'IA
        """
        ### Cas 2: Maximiser --->
        best_eval = float('-inf')
        moves, blocks = generate_moves_and_blocks(board,IA_CASE)
        # D'abord le joueur bouge, ce qui crée un nouveau plateau pour bloquer ensuite
        for move in range(len(moves)):
            ## on prend la liste des WALL_CASE disponible pour ce mouvement !!!!!!!
            blocks_list=blocks[move]
            new_board = make_move(board, moves[move], IA_CASE)
            # On prend un wall_case pour l'associer au mouvement
            for block in blocks_list:
                new_board_with_block = place_block(new_board, block)

                evaluation = minmax(depth + 1, alpha, beta, False,new_board_with_block)
                #best_eval = max(best_eval, evaluation)
                if(best_eval<evaluation):
                    best_board=np.array(new_board_with_block)
                    best_eval=evaluation
                alpha = max(alpha, best_eval)
                #optimisation alpha beta
                if beta < alpha:
                    minmax_board = best_board
                    return best_eval
        minmax_board = best_board
        return best_eval
    else:
        ### Cas 3:Minimiser --->
        """
        L'algorithme cherche a minimiser le joueur  
        """
        worst_eval = float('inf')
        moves, blocks = generate_moves_and_blocks(board, JOUEUR_CASE)

        for move in range(len(moves)):
            blocks_list=blocks[move]
            new_board = make_move(board, moves[move],JOUEUR_CASE)
            for block in blocks_list:
                new_board_with_block = place_block(new_board, block)

                evaluation = minmax(depth + 1, alpha, beta, True,new_board_with_block )

                if(worst_eval>evaluation):
                    best_board = np.array(new_board_with_block)
                    worst_eval=evaluation
                beta = min(beta, worst_eval)
                if beta <= alpha:
                    minmax_board = best_board
                    return worst_eval
        minmax_board = best_board
        return worst_eval

