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
    player_position = np.array(np.where(board == JOUEUR_CASE)).reshape((2, 1))
    player_pos = [player_position[0][0] + 1, player_position[1][0] + 1]
    moves = []
    blocks = []

    # Les directions que peut faire l'IA ou le joueur
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    for dir_row, dir_col in directions:
        new_row = player_position[0] + dir_row
        new_col = player_position[1] + dir_col
        if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]) and board[new_row][new_col] == 0:
            moves.append((new_row, new_col))

    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell == 0 and (row_idx, col_idx) != player_position:
                blocks.append((row_idx, col_idx))

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
"""


def evaluate_board(board):
    # Simple heuristic: count the number of empty cells
    empty_cells = sum(row.count(0) for row in board)
    return empty_cells


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
    pour maximiser
    """
    if maximizing_player:
        max_eval = float('-inf')
        moves, blocks = generate_moves_and_blocks(board, player1)

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
