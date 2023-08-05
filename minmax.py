import numpy as np

FREE_CASE=0
JOUEUR_CASE=1
IA_CASE=2
WALL_CASE=-1




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
    pl_pos = np.array(np.where(board == PLAYER_TYPE)).reshape((2, 1))
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






def generate_moves_and_blocks(board, PLAYER_TYPE):
    # Obtient la position du joueur/IA
    player_position = np.array(np.where(board == PLAYER_TYPE)).reshape((2, 1))
    player_pos = [player_position[0][0] + 1, player_position[1][0] + 1]
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
        print(x, y)
        print(pl_pos)
        if ( (pl_pos[1] + x < 0) or (pl_pos[1] + x > 6) or (pl_pos[0] + y < 0) or (pl_pos[0] + y > 6) ):
            continue
        else:
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

    # Ajoute tout les positions des cellules vides (endroit pour bloquer)
    empty_cells=np.array(np.where(board == FREE_CASE))
    #[ [y,x],[y1,x1], .... ]
    empty_cells=[ [empty_cells[0][i],empty_cells[1][i]] for i in range(len(empty_cells[0]))]
    print(empty_cells)
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


def evaluate_board(board):
    # Simple heuristic: count the number of empty cells
    #empty_cells = sum(row.count(0) for row in board)
    #return empty_cells


    return

def minmax(node, depth, alpha, beta, maximizing_player):
    """
    :param node: noeud racine
    :param depth: profondeur
    :param alpha: meilleur maximimum
    :param beta: meilleur minimum
    :param maximizing_player: est ce qu'on maximise ?
    :return:
    """

    ### Cas 1: Profondeur==0 --> recursion finale
    if depth == 0:
        node.value = evaluate_board(board)
        return node.value

    ### Cas 2: Maximiser --->
    """
    L'algoritme itere tous les cas possible
    pour maximiser l'IA
    """
    if maximizing_player:
        max_eval = float('-inf')
        moves, blocks = generate_moves_and_blocks(board,JOUEUR_CASE)



        # D'abord le joueur bouge, ce qui crée un nouveau plateau pour bloquer ensuite
        for move in moves:
            new_board = make_move(board, move)
            for block in blocks:
                new_board_with_block = place_block(new_board, block)
                child_node = Node(0)  # Create a new child node
                node.child_nodes.append(child_node)
                node.child_count += 1
                evaluation = minmax(child_node, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                #optimisation alpha beta
                if beta <= alpha:
                    break  # Beta cut-off
        return max_eval
    else:
        ### Cas 3:Minimiser --->
        """
        L'algorithme cherche a minimiser le joueur  
        """
        min_eval = float('inf')
        moves, blocks = generate_moves_and_blocks(board, player2)

        for move in moves:
            new_board = make_move(board, move)
            for block in blocks:
                new_board_with_block = place_block(new_board, block)
                child_node = Node(0)  # Create a new child node
                node.child_nodes.append(child_node)
                node.child_count += 1
                evaluation = minmax(child_node, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break  # Alpha cut-off
        return min_eval
