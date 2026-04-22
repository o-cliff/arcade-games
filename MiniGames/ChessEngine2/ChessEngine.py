class GameState:
    def __init__(self):
        # board is 8x8 2d list, each element has 2 characters - colour then piece
        self.board = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
        ]
        # maps every letter to given function for their moves
        self.move_functions = {'p': self.get_pawn_moves, 'r': self.get_rook_moves, 'n': self.get_knight_moves,
                               'b': self.get_bishop_moves, 'q': self.get_queen_moves, 'k': self.get_king_moves}
        # for player move turn
        self.white_to_move = True
        # move history for redoing
        self.move_history = []

        # white and black king location for returning valid moves
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

        self.checks = []
        self.pins = []
        self.in_check = False

        # positions that signal game is over
        self.checkmate = False
        self.stalemate = False

        # co-ordinates for the square where en passant capture is possible
        self.en_passant_possible = ()

        # castling rights
        self.castle_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.castle_rights.wks, self.castle_rights.bks,
                                               self.castle_rights.wqs, self.castle_rights.bqs)]

    def make_move(self, move, notation=False):
        # making a move
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.white_to_move = not self.white_to_move
        self.move_history.append(move)

        # update kings position
        if move.piece_moved == 'wk':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bk':
            self.black_king_location = (move.end_row, move.end_col)

        # pawn promotion
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'q'

        # en passant
        if move.is_en_passant_move:
            self.board[move.start_row][move.end_col] = '--'  # capturing pawn

        # updating en passant possible
        if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:  # only on 2 square pawn advances
            self.en_passant_possible = ((move.start_row + move.end_row)//2, move.end_col)
        else:
            self.en_passant_possible = ()

        # castle move
        if move.is_castle_move:
            if move.end_col - move.start_col == 2:  # king side castle
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = '--'
            else:  # queen side castle
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                self.board[move.end_row][move.end_col - 2] = '--'

        # updating castling rights on rook or king move
        self.update_castle_rights(move)

        # printing notation
        if notation:
            movelog = move.get_chess_notation(move.is_castle_move,
                                            self.square_under_attack(self.black_king_location[0], self.black_king_location[1]) or
                                            self.square_under_attack(self.white_king_location[0], self.white_king_location[1]))
            if move.piece_moved[0] == 'w':
                print(str(len(self.move_history) // 2 + 1) + '. ' + str(movelog), end=' ')
            else:
                print(movelog)

    def undo_move(self, notation=False):
        # redoing a move
        if len(self.move_history) != 0:
            move = self.move_history.pop()
            self.white_to_move = not self.white_to_move
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured

            # update kings position
            if move.piece_moved == 'wk':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bk':
                self.black_king_location = (move.start_row, move.start_col)

            # undoing en passant
            if move.is_en_passant_move:
                self.board[move.end_row][move.end_col] = '--'
                self.board[move.start_row][move.end_col] = move.piece_captured
                self.en_passant_possible = (move.end_row, move.end_col)

            # undo 2 square pawn advance
            if move.piece_moved[0] == 'p' and abs(move.start_row - move.end_row) == 2:
                self.en_passant_possible = ()

            # undoing castle move
            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  # king side
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = '--'
                else:  # queen side
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = '--'

            # undoing castle rights
            self.castle_rights_log.pop()
            self.castle_rights = self.castle_rights_log[-1]

            # fixing notation
            if notation:
                print()

    def update_castle_rights(self, move):
        if move.piece_moved == 'wk':
            self.castle_rights.wks = False
            self.castle_rights.wqs = False
        elif move.piece_moved == 'bk':
            self.castle_rights.bks = False
            self.castle_rights.bqs = False
        elif move.piece_moved == 'wr':
            if move.start_col == 0 and move.start_row == 7:
                self.castle_rights.wqs = False
            if move.start_col == 7 and move.start_row == 7:
                self.castle_rights.wks = False
        elif move.piece_moved == 'br':
            if move.start_col == 0 and move.start_row == 0:
                self.castle_rights.bqs = False
            if move.start_col == 7 and move.start_row == 0:
                self.castle_rights.bks = False

        self.castle_rights_log.append(CastleRights(self.castle_rights.wks, self.castle_rights.bks,
                                                   self.castle_rights.wqs, self.castle_rights.bqs))

    def get_valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1:  # only one possible check
                moves = self.get_all_possible_moves()
                if self.white_to_move:
                    self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves, 'w')
                else:
                    self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves, 'b')

                # to block a check you must move a piece in between king and checking piece
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]  # enemy piece causing the check
                valid_squares = []  # squares that pieces can move to

                # no blocks for knight
                if piece_checking[1] == 'n':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:  # once for loop reaches checking piece
                            break

                # gets rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):  # go through list backwards
                    if moves[i].piece_moved[1] != 'k':  # move doesn't move king so it must block or capture
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:  # moves doesn't either block check or capture piece
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.get_king_moves(king_row, king_col, moves)
        else:  # not in check so all moves are fine
            moves = self.get_all_possible_moves()
            if self.white_to_move:
                self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves, 'w')
            else:
                self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves, 'b')

        return moves

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns in given rows
                turn = self.board[r][c][0]  # gets first character of piece
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)
        return moves

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def check_for_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        if self.white_to_move:
            enemy_colour = 'b'
            ally_colour = 'w'
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_colour = 'w'
            ally_colour = 'b'
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]

        # check outwards from king for pins and checks, keeping track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()  # resetting possible pins
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_colour and end_piece[1] != 'k':
                        if possible_pin == ():  # list with allied pieces that could be pinned
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:  # second allied piece, so no pin possible
                            break
                    elif end_piece[0] == enemy_colour:
                        type = end_piece[1]

                        # many possibilities of check
                        if (0 <= j <= 3 and type == 'r') or \
                                (4 <= j <= 7 and type == 'b') or \
                                (i == 1 and type == 'p' and ((enemy_colour == 'w' and 6 <= j <= 7) or
                                                             (enemy_colour == 'b' and 4 <= j <= 5))) or \
                                (type == 'q') or (i == 1 and type == 'k'):
                            if possible_pin == ():  # no piece blocking, so check
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:  # a piece is blocking, so it is pinned
                                pins.append(possible_pin)
                                break
                        else:  # enemy piece isn't checking you
                            break
                else:  # move is off the board
                    break

        # now checks for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_colour and end_piece[1] == 'n':  # night attacking king
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))

        return in_check, pins, checks

    def square_under_attack(self, row, col):
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opp_moves:
            if move.end_row == row and move.end_col == col:
                return True
        return False

    def get_pawn_moves(self, row, col, moves):
        piece_pinned = False
        pin_dir = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:  # white pawn moves
            if self.board[row - 1][col] == '--':  # one square pawn advance
                if not piece_pinned or pin_dir == (-1, 0):  # checks for pinned piece
                    moves.append(Move((row, col), (row - 1, col), self.board))
                    if row == 6 and self.board[row - 2][col] == '--':  # two square pawn advance
                        moves.append(Move((row, col), (row - 2, col), self.board))

            # captures
            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b':  # capturing to the left
                    if not piece_pinned or pin_dir == (-1, -1):  # checks for pinned piece
                        moves.append(Move((row, col), (row - 1, col - 1), self.board))
                if (row-1, col-1) == self.en_passant_possible:  # en passant moves
                    moves.append(Move((row, col), (row - 1, col - 1), self.board, en_passant_move=True))
            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == 'b':  # capturing to the right
                    if not piece_pinned or pin_dir == (-1, 1):  # checks for pinned piece
                        moves.append(Move((row, col), (row - 1, col + 1), self.board))
                if (row-1, col+1) == self.en_passant_possible:  # en passant moves
                    moves.append(Move((row, col), (row - 1, col + 1), self.board, en_passant_move=True))

        if not self.white_to_move:  # black pawn moves
            if self.board[row + 1][col] == '--':  # one square pawn advance
                if not piece_pinned or pin_dir == (1, 0):  # checks for pinned piece
                    moves.append(Move((row, col), (row + 1, col), self.board))
                    if row == 1 and self.board[row + 2][col] == '--':  # two square pawn advance
                        moves.append(Move((row, col), (row + 2, col), self.board))

            # captures
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':  # capturing to the left
                    if not piece_pinned or pin_dir == (1, -1):  # checks for pinned piece
                        moves.append(Move((row, col), (row + 1, col - 1), self.board))
                if (row+1, col-1) == self.en_passant_possible:  # en passant moves
                    moves.append(Move((row, col), (row + 1, col - 1), self.board, en_passant_move=True))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':  # capturing to the right
                    if not piece_pinned or pin_dir == (1, 1):  # checks for pinned piece
                        moves.append(Move((row, col), (row + 1, col + 1), self.board))
                if (row+1, col+1) == self.en_passant_possible:  # en passant moves
                    moves.append(Move((row, col), (row + 1, col + 1), self.board, en_passant_move=True))

    def get_rook_moves(self, row, col, moves):
        piece_pinned = False
        pin_dir = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != 'q':  # queens only remove if on bishop pin
                    self.pins.remove(self.pins[i])
                break

        for dist in range(1, len(self.board)):  # rooks travelling down
            if not piece_pinned or pin_dir == (1, 0) or pin_dir == (-1, 0):
                if row + dist > 7:
                    break
                if self.board[row + dist][col] == '--':  # if blank square
                    moves.append(Move((row, col), (row + dist, col), self.board))
                if self.board[row + dist][col][0] != self.board[row][col][0] and self.board[row + dist][col][0] != '-':  # if piece is opposite colour
                    moves.append(Move((row, col), (row + dist, col), self.board))
                    break
                if self.board[row + dist][col][0] == self.board[row][col][0]:  # if piece is same colour
                    break

        for dist in range(1, len(self.board)):  # rooks travelling up
            if not piece_pinned or pin_dir == (-1, 0) or pin_dir == (1, 0):
                if row - dist < 0:
                    break
                if self.board[row - dist][col] == '--':  # if blank square
                    moves.append(Move((row, col), (row - dist, col), self.board))
                if self.board[row - dist][col][0] != self.board[row][col][0] and self.board[row - dist][col][0] != '-':  # if piece is opposite colour
                    moves.append(Move((row, col), (row - dist, col), self.board))
                    break
                if self.board[row - dist][col][0] == self.board[row][col][0]:  # if piece is same colour
                    break

        for dist in range(1, len(self.board)):  # rooks travelling right
            if not piece_pinned or pin_dir == (0, 1) or pin_dir == (0, -1):
                if col + dist > 7:
                    break
                if self.board[row][col + dist] == '--':  # if blank square
                    moves.append(Move((row, col), (row, col + dist), self.board))
                if self.board[row][col + dist][0] != self.board[row][col][0] and self.board[row][col + dist][0] != '-':  # if piece is opposite colour
                    moves.append(Move((row, col), (row, col + dist), self.board))
                    break
                if self.board[row][col + dist][0] == self.board[row][col][0]:  # if piece is same colour
                    break

        for dist in range(1, len(self.board)):  # rooks travelling left
            if not piece_pinned or pin_dir == (0, -1) or pin_dir == (0, 1):
                if col - dist < 0:
                    break
                if self.board[row][col - dist] == '--':  # if blank square
                    moves.append(Move((row, col), (row, col - dist), self.board))
                if self.board[row][col - dist][0] != self.board[row][col][0] and self.board[row][col - dist][0] != '-':  # if piece is opposite colour
                    moves.append(Move((row, col), (row, col - dist), self.board))
                    break
                if self.board[row][col - dist][0] == self.board[row][col][0]:  # if piece is same colour
                    break

    def get_knight_moves(self, row, col, moves):
        piece_pinned = False
        pin_dir = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if not piece_pinned:
            if row + 2 <= 7:
                if col + 1 <= 7:
                    if self.board[row + 2][col + 1][0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (row + 2, col + 1), self.board))
                if col - 1 >= 0:
                    if self.board[row + 2][col - 1][0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (row + 2, col - 1), self.board))

            if row - 2 >= 0:
                if col + 1 <= 7:
                    if self.board[row - 2][col + 1][0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (row - 2, col + 1), self.board))
                if col - 1 >= 0:
                    if self.board[row - 2][col - 1][0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (row - 2, col - 1), self.board))

            if col + 2 <= 7:
                if row + 1 <= 7:
                    if self.board[row + 1][col + 2][0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (row + 1, col + 2), self.board))
                if row - 1 >= 0:
                    if self.board[row - 1][col + 2][0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (row - 1, col + 2), self.board))

            if col - 2 >= 0:
                if row + 1 <= 7:
                    if self.board[row + 1][col - 2][0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (row + 1, col - 2), self.board))
                if row - 1 >= 0:
                    if self.board[row - 1][col - 2][0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (row - 1, col - 2), self.board))

    def get_bishop_moves(self, row, col, moves):
        piece_pinned = False
        pin_dir = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        for dist in range(1, len(self.board)):
            if not piece_pinned or pin_dir == (1, 1) or pin_dir == (-1, -1):
                if row + dist > 7 or col + dist > 7:
                    break
                if self.board[row + dist][col + dist] == '--':
                    moves.append(Move((row, col), (row + dist, col + dist), self.board))
                if self.board[row + dist][col + dist][0] != self.board[row][col][0] and self.board[row + dist][col + dist][0] != '-':
                    moves.append(Move((row, col), (row + dist, col + dist), self.board))
                    break
                if self.board[row + dist][col + dist][0] == self.board[row][col][0]:
                    break

        for dist in range(1, len(self.board)):
            if not piece_pinned or pin_dir == (-1, -1) or pin_dir == (1, 1):
                if row - dist < 0 or col - dist < 0:
                    break
                if self.board[row - dist][col - dist] == '--':
                    moves.append(Move((row, col), (row - dist, col - dist), self.board))
                if self.board[row - dist][col - dist][0] != self.board[row][col][0] and self.board[row - dist][col - dist][0] != '-':
                    moves.append(Move((row, col), (row - dist, col - dist), self.board))
                    break
                if self.board[row - dist][col - dist][0] == self.board[row][col][0]:
                    break

        for dist in range(1, len(self.board)):
            if not piece_pinned or pin_dir == (-1, 1) or pin_dir == (1, -1):
                if row - dist < 0 or col + dist > 7:
                    break
                if self.board[row - dist][col + dist] == '--':
                    moves.append(Move((row, col), (row - dist, col + dist), self.board))
                if self.board[row - dist][col + dist][0] != self.board[row][col][0] and self.board[row - dist][col + dist][0] != '-':
                    moves.append(Move((row, col), (row - dist, col + dist), self.board))
                    break
                if self.board[row - dist][col + dist][0] == self.board[row][col][0]:
                    break

        for dist in range(1, len(self.board)):
            if not piece_pinned or pin_dir == (1, -1) or pin_dir == (-1, 1):
                if row + dist > 7 or col - dist < 0:
                    break
                if self.board[row + dist][col - dist] == '--':
                    moves.append(Move((row, col), (row + dist, col - dist), self.board))
                if self.board[row + dist][col - dist][0] != self.board[row][col][0] and self.board[row + dist][col - dist][0] != '-':
                    moves.append(Move((row, col), (row + dist, col - dist), self.board))
                    break
                if self.board[row + dist][col - dist][0] == self.board[row][col][0]:
                    break

    def get_queen_moves(self, row, col, moves):
        piece_pinned = False
        pin_dir = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_colour = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_colour:  # not an ally piece, either opposite or empty
                    if ally_colour == 'w':
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    # place king back to original location
                    if ally_colour == 'w':
                        self.white_king_location = (row, col)
                    else:
                        self.black_king_location = (row, col)

    def get_castle_moves(self, row, col, moves, ally_colour):
        if self.square_under_attack(row, col):
            return
        if (self.white_to_move and self.castle_rights.wks) or (not self.white_to_move and self.castle_rights.bks):
            self.get_king_side_castle_moves(row, col, moves, ally_colour)
        if (self.white_to_move and self.castle_rights.wqs) or (not self.white_to_move and self.castle_rights.bqs):
            self.get_queen_side_castle_moves(row, col, moves, ally_colour)

    def get_king_side_castle_moves(self, r, c, moves, ally_colour):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.square_under_attack(r, c+1) and not self.square_under_attack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, is_castle_move=True))

    def get_queen_side_castle_moves(self, r, c, moves, ally_colour):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.square_under_attack(r, c-1) and not self.square_under_attack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, is_castle_move=True))

    def board_square_to_pos(self, board_num):
        row = board_num // 8
        col = board_num % 8
        return (self.board[row][col], row, col, Move.cols_to_files[col] + Move.rows_to_ranks[row])


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move:
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, en_passant_move=False, is_castle_move=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.board = board
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_pawn_promotion = (self.piece_moved == 'wp' and self.end_row == 0) or (self.piece_moved == 'bp' and self.end_row == 7)
        self.is_en_passant_move = en_passant_move
        self.is_castle_move = is_castle_move

        if self.is_en_passant_move:
            if self.piece_moved == 'wp':
                self.piece_captured = 'bp'
            else:
                self.piece_captured = 'wp'

        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID

    def get_chess_notation(self, is_castle, is_check):
        end_rank_file = self.get_rank_file(self.end_row, self.end_col)
        start_file = self.cols_to_files[self.start_col]
        piece = self.board[self.end_row][self.end_col][1]
        capture = ''
        check = '+' if is_check else ''
        is_castle_move = '0-0' if is_castle else ''
        promotion = '=Q' if self.is_pawn_promotion else ''

        if self.piece_captured != '--':
            capture = 'x'

        if piece != 'p':
            return piece.upper() + capture + end_rank_file + promotion + check
        else:
            if capture:
                return start_file + 'x' + end_rank_file + promotion + check
            else:
                return end_rank_file + promotion + check

    def get_rank_file(self, row, column):
        return self.cols_to_files[column] + self.rows_to_ranks[row]
