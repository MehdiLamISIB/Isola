import numpy as np

FREE_CASE=0
JOUEUR_CASE=1
IA_CASE=2
WALL_CASE=-1



board=[]
minmax_board=[]

class Node():
    def __init__(self, value):
        # Heurestic value
        self.value = value
        self.child_nodes=[]
        self.child_count=0
    def AddNode(self,node):

        self.child_nodes.append(node)
        self.child_count=len(self.child_nodes)

### Fonction peut être utiliser pour Joueur et IA
def check_cell_around(PLAYER_TYPE):
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
        return abs( board[y+1][x]+ board[y+1][x+1]+ board[y][x+1]  )
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

def make_move(board,move,PLAYER_TYPE):
    move_board = board#np.array( np.where(board == PLAYER_TYPE, FREE_CASE, board) )
    old_position=np.array(np.where(board==PLAYER_TYPE))
    move_board[old_position[0][0],old_position[1][0]]=FREE_CASE
    move_board[move[0], move[1]] = PLAYER_TYPE
    return move_board

def place_block(board,block):
    # ajoute le block
    block_board=board
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
    for move in moves:
        # on enleve l'ancienne poisiton
        # et on la replace par la nouvelle position
        move_board=make_move(board, move, PLAYER_TYPE)
        # Ajoute tout les positions des cellules vides (endroit pour bloquer)
        empty_cells=np.array(np.where(move_board == FREE_CASE) ).T
        #[ [y,x],[y1,x1], .... ]
        #empty_cells=[  [empty_cells[0][i],empty_cells[1][i]]  for i in range(len(empty_cells[0])) ]
        blocks.append(empty_cells.tolist())
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
    # Simple heuristic: count the number of empty cells
    #empty_cells = sum(row.count(0) for row in board)
    #return empty_cells

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
        around_adversary_value = check_cell_around(JOUEUR_CASE)
        around_player = check_cell_around(IA_CASE)

    else:
        around_adversary_value = check_cell_around(IA_CASE)
        around_player = check_cell_around(JOUEUR_CASE)

    return 20 * around_adversary_value - 40 * around_player - 35*manthann_distance

def minmax(node, depth, alpha, beta, maximizing_player,board):
    global minmax_board
    """
    :param node: noeud racine
    :param depth: profondeur
    :param alpha: meilleur maximimum
    :param beta: meilleur minimum
    :param maximizing_player: est ce qu'on maximise ?
    :return:
    """
    new_board_with_block=[]
    new_board=[]
    ### Cas 1: Profondeur==0 --> recursion finale, retour de la pile
    if depth == 0:
        if(maximizing_player):
            node.value = evaluate_board(board,IA_CASE)
        else:
            node.value = evaluate_board(board,JOUEUR_CASE)
        #print("DEPTH====0")
        return node.value
    ### Cas 2: Maximiser --->
    """
    L'algoritme itere tous les cas possible
    pour maximiser l'IA
    """
    if maximizing_player:
        max_eval = float('-inf')
        moves, blocks = generate_moves_and_blocks(board,IA_CASE)
        # D'abord le joueur bouge, ce qui crée un nouveau plateau pour bloquer ensuite
        block_list_count=0
        for move in moves:
            ## on prend la liste des WALL_CASE disponible pour ce mouvement !!!!!!!
            block_list_count=block_list_count+1
            blocks_list=blocks[block_list_count]

            new_board=board
            new_board = make_move(board, move, IA_CASE)
            # On prend un wall_case pour l'associer au mouvement
            for block in blocks_list:
                new_board_with_block=new_board
                new_board_with_block = place_block(new_board, block)
                child_node = Node(0)  # Create a new child node
                node.child_nodes.append(child_node)
                node.child_count += 1
                ## Boucle de recursion
                evaluation = minmax(child_node, depth - 1, alpha, beta, False,new_board_with_block)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                #optimisation alpha beta
                if beta <= alpha:
                    break  # Beta cut-off
            #print("MAX MAX")
            minmax_board=new_board
        return max_eval
    else:
        ### Cas 3:Minimiser --->
        """
        L'algorithme cherche a minimiser le joueur  
        """
        min_eval = float('inf')
        moves, blocks = generate_moves_and_blocks(board, JOUEUR_CASE)
        block_list_count = 0

        for move in moves:
            block_list_count=block_list_count+1
            blocks_list=blocks[block_list_count]

            new_board=board
            new_board = make_move(board, move,JOUEUR_CASE)
            for block in blocks_list:
                new_board_with_block = new_board
                new_board_with_block = place_block(new_board, block)
                child_node = Node(0)  # Create a new child node
                node.child_nodes.append(child_node)
                node.child_count += 1
                ## Chaque nouvelle evaluation minmax aura son propre plateau de jeu (Noeud si on veut
                evaluation = minmax(child_node, depth - 1, alpha, beta, True,new_board_with_block)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break  # Alpha cut-off
            #print("MIN MIN")
            minmax_board = new_board
        return min_eval
