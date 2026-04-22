from ChessEngine2 import ChessEngine


def piece_value(piece, x, y):
    if piece == '--':
        return 0
    value = abs_value(piece, x, y)
    if piece[0] == 'w':
        return -1 * value
    else:
        return 1 * value


def abs_value(piece, x, y):
    if piece[1] == 'p':
        return 100 + (pawntablew[x][y] if piece[0] == 'w' else pawntableb[x][y])
    elif piece[1] == 'n':
        return 340 + (knighttablew[x][y] if piece[0] == 'w' else knighttableb[x][y])
    elif piece[1] == 'b':
        return 350 + (bishoptablew[x][y] if piece[0] == 'w' else bishoptableb[x][y])
    elif piece[1] == 'r':
        return 500 + (rooktablew[x][y] if piece[0] == 'w' else rooktableb[x][y])
    elif piece[1] == 'q':
        return 900 + (queentablew[x][y] if piece[0] == 'w' else queentableb[x][y])
    elif piece[1] == 'k':
        return 9000 + (kingtablew[x][y] if piece[0] == 'w' else kingtableb[x][y])


def evaluation(gs):
    eval_f = 0
    for i in range(0, 8):
        for j in range(0, 8):
            eval_t = piece_value(gs.board[i][j], i, j)
            if eval_t:
                eval_f += eval_t

    return eval_f


def minimax_root(depth, gs, is_maximising_player):
    new_game_moves = gs.get_valid_moves()
    best_move = -99999999999999
    best_move_found = None

    for i in range(0, len(new_game_moves)):
        temp_castle = (gs.castle_rights.wks, gs.castle_rights.bks,
                       gs.castle_rights.wqs, gs.castle_rights.bqs)
        temp_log = gs.castle_rights_log
        gs.make_move(new_game_moves[i])
        value = minimax(depth - 1, gs, -100000, 100000, not is_maximising_player)
        gs.undo_move()
        gs.castle_rights = ChessEngine.CastleRights(temp_castle[0], temp_castle[1],
                                                    temp_castle[2], temp_castle[3])
        gs.castle_rights_log = temp_log
        if value >= best_move:
            best_move = value
            best_move_found = new_game_moves[i]

    return best_move_found


def minimax(depth, gs, alpha, beta, is_maximising_player):
    if depth == 0:
        if is_maximising_player:
            return -evaluation(gs)
        else:
            return evaluation(gs)

    new_game_moves = gs.get_valid_moves()
    if len(new_game_moves) == 0:
        if gs.white_to_move:
            if gs.square_under_attack(gs.white_king_location[0], gs.white_king_location[1]):
                return 9999999999
            else:
                return 0
        else:
            if gs.square_under_attack(gs.black_king_location[0], gs.black_king_location[1]):
                return -9999999999
            else:
                return 0

    if is_maximising_player:
        best_move = -9999999
        for i in range(0, len(new_game_moves)):
            temp_castle = (gs.castle_rights.wks, gs.castle_rights.bks,
                           gs.castle_rights.wqs, gs.castle_rights.bqs)
            temp_log = gs.castle_rights_log
            gs.make_move(new_game_moves[i])
            best_move = max(best_move, minimax(
                depth - 1, gs, alpha, beta, not is_maximising_player))
            gs.undo_move()
            gs.castle_rights = ChessEngine.CastleRights(temp_castle[0], temp_castle[1],
                                                        temp_castle[2], temp_castle[3])
            gs.castle_rights_log = temp_log
            alpha = max(alpha, best_move)
            if beta <= alpha:
                return best_move

        return best_move
    else:
        best_move = 9999999
        for i in range(0, len(new_game_moves)):
            temp_castle = (gs.castle_rights.wks, gs.castle_rights.bks,
                           gs.castle_rights.wqs, gs.castle_rights.bqs)
            temp_log = gs.castle_rights_log
            gs.make_move(new_game_moves[i])
            best_move = min(best_move, minimax(
                depth - 1, gs, alpha, beta, not is_maximising_player))
            gs.undo_move()
            gs.castle_rights = ChessEngine.CastleRights(temp_castle[0], temp_castle[1],
                                                        temp_castle[2], temp_castle[3])
            gs.castle_rights_log = temp_log
            beta = min(beta, best_move)
            if beta <= alpha:
                return best_move

        return best_move


pawntableb = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [0, 0, 0, 40, 40, 0, 0, 0],
    [5, 5, 10, 45, 45, 10, 5, 5],
    [10, 10, 20, 50, 50, 20, 10, 10],
    [50, 50, 50, 55, 55, 50, 50, 50],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
pawntablew = list(reversed(pawntableb))

knighttableb = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, 5, 10, 15, 15, 10, 5, -50],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-40, 20, 0, 0, 0, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]
knighttablew = list(reversed(knighttableb))

bishoptableb = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 0, 15, 10, 15, 10, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [10, 0, 0, 0, 0, 0, 0, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]
bishoptablew = list(reversed(bishoptableb))

rooktableb = [
    [0, 0, 0, 5, 5, 0, 0, 0],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
rooktablew = list(reversed(rooktableb))

queentableb = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 15, 5, 5, 5, 5, 10, -10],
    [-10, 0, 5, 5, 5, 5, 0, -5],
    [-5, -5, 5, 5, 5, 5, 0, -5],
    [-10, 10, 5, 5, 5, 5, 10, -10],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
]
queentablew = list(reversed(queentableb))

kingtableb = [
    [20, 30, 10, 0, 0, 10, 30, 20],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30]
]
kingtablew = list(reversed(kingtableb))
