from tictacchess import *

# 77

## Funções auxiliares

def aux_opponent_77(player):
    """Retorna o oponente do jogador"""

    return 'BLACK' if player == 'WHITE' else 'WHITE'

def aux_has_n_same_line_77(estado, p, n):
    """Verifica se o jogador p tem n peças na mesma linha, coluna ou diagonal"""

    state = copy.deepcopy(estado)
    p_cells, _ = state.player_used_cells(p)

    # scan board and see if there's n in the same line
    for cell in p_cells:
        line = cell[0]
        column = cell[1]

        # Check lines
        if sum([1 for i in range(4) if (line, i) in p_cells]) == n:
            return True
        
        # Check columns
        if sum([1 for i in range(4) if (i, column) in p_cells]) == n:
            return True
        
        # Check diagonals
        if line == column:
            if sum([1 for i in range(4) if (i, i) in p_cells]) == n:
                return True
        elif line + column == 3:
            if sum([1 for i in range(4) if (i, 3-i) in p_cells]) == n:
                return True
            
    return False

def aux_has_n_in_line_from_cell_77(state, opponent, cell, n):
    """
    Checks if the opponent has exactly 2 pieces in a line that includes the specified cell.
    """
    opponent_cells, _ = state.player_used_cells(opponent)
    x, y = cell
    
    # Check for two in the row that includes the cell
    row_count = sum((x, col) in opponent_cells for col in range(4))
    if row_count >= n:
        return True
    
    # Check for two in the column that includes the cell
    col_count = sum((row, y) in opponent_cells for row in range(4))
    if col_count >= n:
        return True
    
    # Check for two in the primary diagonal (if the cell is on it)
    if x == y:
        diag_count = sum((i, i) in opponent_cells for i in range(4))
        if diag_count >= n:
            return True
    
    # Check for two in the secondary diagonal (if the cell is on it)
    if x + y == 3:
        anti_diag_count = sum((i, 3 - i) in opponent_cells for i in range(4))
        if anti_diag_count >= n:
            return True

    return False

def aux_fixed_possible_moves_77(estado,piece,player):
        estado = copy.deepcopy(estado)
        loc = estado.board[piece]
        if piece == 'C' or piece == 'c':
            list_moves = aux_fixed_knight_possible_moves_77(estado, loc, player)
        if piece == 'B' or piece == 'b':
            directions = [(+1,+1),(+1,-1),(-1,+1),(-1,-1)]
            list_moves = aux_fixed_bishop_rook_possible_moves_77(estado, loc,directions, player)
        if piece == 'T' or piece == 't':
            directions = [(+1,0),(-1,0),(0,+1),(0,-1)]
            list_moves = aux_fixed_bishop_rook_possible_moves_77(estado, loc,directions, player)
        if piece == 'P' or piece =='p': 
            list_moves = aux_fixed_pawn_possible_moves_77(estado,piece,loc,player)
        list_moves = [(piece,mov) for mov in list_moves]   
        return list_moves
    
def aux_fixed_knight_possible_moves_77(estado,loc,player):
    # list all new locations based on piece behavior:
    deltas = [(+1,+2),(+1,-2),(-1,+2),(-1,-2),(+2,+1),(+2,-1),(-2,+1),(-2,-1)]
    movements = [(loc[0]+delta[0], loc[1]+delta[1]) for delta in deltas]
    # filter out the locations outside the board:
    movements = [(x,y) for (x,y) in movements if x in range(estado.h) and y in range(estado.v)]
    # filter out the locations on top of own's pieces:
    my_cells,_ = estado.player_used_cells(player)
    movements = [(x,y) for (x,y) in movements if (x,y) not in my_cells]
    return movements

def aux_fixed_bishop_rook_possible_moves_77(estado,loc,directions,player):
    movements = []
    # list all new locations on all directions still within the board:
    for delta in directions:
        x = loc[0] + delta[0]
        y = loc[1] + delta[1]
        while x in range(estado.h) and y in range(estado.v):
            if (x,y) in estado.board.values():
                opponent_cells,_ = estado.player_used_cells(aux_opponent_77(player))
                if (x,y) in opponent_cells:
                    movements.append((x,y))
                break
            else:
                movements.append((x,y))
                x += delta[0]
                y += delta[1]
    return movements

def aux_fixed_pawn_possible_moves_77(estado,piece,loc,player):
    # list all new locations based on piece behavior:
    # (need to know which direction (+1 or -1) the pawn is moving, and whether there are opponents in possible new locs)
    if piece == 'P': # to_move is WHITE
        new_straight_loc = (loc[0]-estado.pawn_direction[0],loc[1])
        new_diagonal_loc1 = (loc[0]-estado.pawn_direction[0],loc[1]+1)
        new_diagonal_loc2 = (loc[0]-estado.pawn_direction[0],loc[1]-1)
    else:
        #new_straight_loc = (loc[0]+self.pawn_direction[0],loc[1])
        #new_diagonal_loc1 = (loc[0]+self.pawn_direction[0],loc[1]+1)
        #new_diagonal_loc2 = (loc[0]+self.pawn_direction[0],loc[1]-1)           
        new_straight_loc = (loc[0]+estado.pawn_direction[1],loc[1])
        new_diagonal_loc1 = (loc[0]+estado.pawn_direction[1],loc[1]+1)
        new_diagonal_loc2 = (loc[0]+estado.pawn_direction[1],loc[1]-1)           
    movements = []
    if new_straight_loc not in estado.board.values(): # pawn can only move if no one is blocking it
        movements.append(new_straight_loc)
    opponent_cells, opponent_pieces = estado.player_used_cells(aux_opponent_77(player))
    if new_diagonal_loc1 in opponent_cells: # pawn can move diagonally to take an opponent's piece
        movements.append(new_diagonal_loc1) 
    if new_diagonal_loc2 in opponent_cells:
        movements.append(new_diagonal_loc2) 
    # filter out the locations outside the board:
    movements = [(x,y) for (x,y) in movements if x in range(estado.h) and y in range(estado.v)]
    return movements

## Heurísticas

def heuristic_winner_77(estado, player):
    """Heurística que verifica se o jogador ganhou o jogo"""

    state = copy.deepcopy(estado)
    opponent = aux_opponent_77(player)
    
    WIN_SCORE = infinity

    winner = state.have_winner()
    if winner == player:
        return WIN_SCORE
    if winner == opponent:
        return -WIN_SCORE
    
    return 0

def heuristic_in_row_77(estado, player):
    """Heurística que verifica se o jogador tem 3 ou 2 peças em linha"""

    state = copy.deepcopy(estado)
    score = 0
    opponent = aux_opponent_77(player)

    THREE_IN_ROW_SCORE = 5
    TWO_IN_ROW_SCORE = 3

    if aux_has_n_same_line_77(state, opponent, 3):
        score -= THREE_IN_ROW_SCORE
    elif aux_has_n_same_line_77(state, player, 3):
        score += THREE_IN_ROW_SCORE
        pass

    return score

def heuristic_empty_cell_line_77(estado, player):
    """Heurística que verifica se o oponente tem uma linha com 3 peças e uma célula vazia. Se tiver, penaliza o jogador."""

    state = copy.deepcopy(estado)
    opponent = aux_opponent_77(player)
    score = 0

    # penalty for having an having an empty cell in a opponent line with 3 pieces
    EMPTY_CELL_LINE_PENALTY = 5

    def check_lines(pl_cells, op_cells):
        visited_lines = []
        s = 0

        for cell in op_cells:
            # go through all used cells, see if there are at least 3 pieces in that same line
            line = cell[0]
            if line in visited_lines:
                continue

            # check if there are 3 pieces in that line
            if sum([1 for i in range(4) if (line, i) in op_cells]) == 3:
                # check if there's an empty cell in that line
                # if there is, then it's a bad move
                for i in range(4):
                    if (line, i) not in pl_cells and (line, i) not in op_cells:
                        s -= EMPTY_CELL_LINE_PENALTY
                        break

            visited_lines.append(line)

        return s
    
    def check_columns(pl_cells, op_cells):
        visited_columns = []
        s = 0

        for cell in op_cells:
            # go through all used cells, see if there are at least 3 pieces in that same column
            column = cell[1]
            if column in visited_columns:
                continue

            # check if there are 3 pieces in that column
            if sum([1 for i in range(4) if (i, column) in op_cells]) == 3:
                # check if there's an empty cell in that column
                # if there is, then it's a bad move
                for i in range(4):
                    if (i, column) not in pl_cells and (i, column) not in op_cells:
                        s -= EMPTY_CELL_LINE_PENALTY
                        break

            visited_columns.append(column)

        return s
    
    def check_diagonals(pl_cells, op_cells):
        s = 0

        # check if there are 3 pieces in the diagonal
        if sum([1 for i in range(4) if (i, i) in op_cells]) == 3:
            # check if there's an empty cell in the diagonal
            for i in range(4):
                if (i, i) not in pl_cells and (i, i) not in op_cells:
                    s -= EMPTY_CELL_LINE_PENALTY
                    break

        if sum([1 for i in range(4) if (i, 3-i) in op_cells]) == 3:
            # check if there's an empty cell in the diagonal
            for i in range(4):
                if (i, 3-i) not in pl_cells and (i, 3-i) not in op_cells:
                    s -= EMPTY_CELL_LINE_PENALTY
                    break

        return s

    # Check if the opponent has three in a row
    if aux_has_n_same_line_77(state, opponent, 3):
        op_cells, _ = state.player_used_cells(opponent)
        pl_cells, _ = state.player_used_cells(player)

        # Figure out if the player is blocking any 3 in a rows with a piece in the middle
        score += check_lines(pl_cells, op_cells)
        score += check_columns(pl_cells, op_cells)
        score += check_diagonals(pl_cells, op_cells)

    return score

def heuristic_center_77(estado, jogador):
    """Heurística que recompensa o jogador por ter peças nas casas centrais"""

    state = copy.deepcopy(estado)
    opponent = aux_opponent_77(jogador)
    score = 0

    CENTER_SCORE = 2.5
    CENTER_PENALTY = 2.5

    player_cells, _ = state.player_used_cells(jogador)
    for cell in player_cells:
        line = cell[0]
        column = cell[1]

        if line == 1 and column == 1:
            score += CENTER_SCORE
        elif line == 1 and column == 2:
            score += CENTER_SCORE
        elif line == 2 and column == 1:
            score += CENTER_SCORE
        elif line == 2 and column == 2:
            score += CENTER_SCORE

    opponent_cells, _ = state.player_used_cells(opponent)
    for cell in opponent_cells:
        line = cell[0]
        column = cell[1]

        if line == 1 and column == 1:
            score -= CENTER_PENALTY
        elif line == 1 and column == 2:
            score -= CENTER_PENALTY
        elif line == 2 and column == 1:
            score -= CENTER_PENALTY
        elif line == 2 and column == 2:
            score -= CENTER_PENALTY

    return score

def heuristic_mobility_77(estado, jogador):
    """Heurística que recompensa o jogador por ter mais mobilidade"""

    state = copy.deepcopy(estado)
    opponent = aux_opponent_77(jogador)

    MOBILITY_SCORE = 2

    player_pieces = state.player_used_pieces(jogador)
    opponent_pieces = state.player_used_pieces(opponent)

    player_moves = 0
    opponent_moves = 0

    for piece in player_pieces:
        player_moves += len(aux_fixed_possible_moves_77(state, piece, jogador))
    
    for piece in opponent_pieces:
        opponent_moves += len(aux_fixed_possible_moves_77(state, piece, opponent))

    return (player_moves - opponent_moves) * MOBILITY_SCORE

def heuristic_one_piece_77(estado, jogador):
    """Heurística que recompensa o jogador por ter pelo menos uma peça disponível caso não tenha 3 em linha"""

    ONE_PIECE_SCORE = 3

    state = copy.deepcopy(estado)
    used_pieces = state.player_used_pieces(jogador)
    player_pieces = state.player_pieces(jogador)
    unused_pieces = [piece for piece in player_pieces if piece not in used_pieces]

    if aux_has_n_same_line_77(state, jogador, 3):
        return 0
    
    return ONE_PIECE_SCORE if len(unused_pieces) > 0 else -ONE_PIECE_SCORE

def heuristic_more_pieces_77(estado, jogador):
    """Heurística que recompensa o jogador por ter mais peças que o oponente"""

    state = copy.deepcopy(estado)
    player_pieces = state.player_used_pieces(jogador)
    opponent_pieces = state.player_used_pieces(aux_opponent_77(jogador))

    PIECE_SCORE = 1.5

    return (len(player_pieces) - len(opponent_pieces)) * PIECE_SCORE

def heuristic_defensive_77(estado, jogador):
    """Heurística que recompensa a defesa do jogador e penaliza a defesa eficiente do oponente."""
    
    state = copy.deepcopy(estado)
    player = jogador
    opponent = aux_opponent_77(player)

    DEFENSIVE_SCORE = 3
    DEFENSIVE_PENALTY = 3
    OCCUPIED_CELL_SCORE = 1

    num_board_cells = 16

    # Defesa do jogador
    player_cells, _ = state.player_used_cells(player)
    player_pieces = state.player_used_pieces(player)
    defensive_score = 0

    protected_cells = set()
    for piece in player_pieces:
        for _, move in aux_fixed_possible_moves_77(state, piece, player):
            if move in player_cells:
                defensive_score += DEFENSIVE_SCORE
                protected_cells.add(move)

    opponent_cells, _ = state.player_used_cells(opponent)
    opponent_pieces = state.player_used_pieces(opponent)
    defensive_penalty = 0

    for piece in opponent_pieces:
        for _, move in aux_fixed_possible_moves_77(state, piece, opponent):
            if move in opponent_cells:
                defensive_penalty -= DEFENSIVE_PENALTY

    board_score = len(protected_cells) / num_board_cells * OCCUPIED_CELL_SCORE

    return defensive_score + defensive_penalty + board_score

def heuristic_threat_77(estado, jogador):
    """Heuristica que, caso o oponente tenha 2 ou mais peças em uma linha, o player tem que ter sempre uma peça que ameace essa linha (uma peça que tenha um movimento que capture uma peça do adversário que faça parte dessa linha). Caso contrário, penaliza o player"""

    # Find the opponent cells that are part of at least 2-piece lines and increase the score if the player has a piece which has at least one possible move that is part of the cells. That will mean the piece is attacking the piece in the line which is good. 

    state = copy.deepcopy(estado)
    player = jogador
    opponent = aux_opponent_77(player)

    THREAT_PENALTY = 5
    THREAT_REWARD = 5
    score = 0

    # Check if the opponent has 2 in a row
    opponent_cells, _ = state.player_used_cells(opponent)
    cells_to_threaten = [cell for cell in opponent_cells if aux_has_n_in_line_from_cell_77(state, opponent, cell, 2)]

    for piece in state.player_used_pieces(player):
        for _, move in aux_fixed_possible_moves_77(state, piece, player):
            if move in cells_to_threaten:
                cells_to_threaten.remove(move)
                score += THREAT_REWARD

    score -= len(cells_to_threaten) * THREAT_PENALTY

    return score

def func_77(estado, jogador):
    heuristics = [
        heuristic_winner_77,
        heuristic_in_row_77,
        heuristic_empty_cell_line_77,
        heuristic_center_77,
        heuristic_mobility_77,
        heuristic_one_piece_77,
        heuristic_more_pieces_77,
        heuristic_defensive_77,
        heuristic_threat_77
    ]   

    return sum([h(estado, jogador) for h in heuristics])