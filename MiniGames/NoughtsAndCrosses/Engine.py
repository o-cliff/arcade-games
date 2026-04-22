class GameState:
    def __init__(self):
        self.board = [
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']
        ]

        self.player_1_to_move = True
        self.win = False
        self.draw = False
        self.move_history = []

    def get_win(self):
        for i in range(len(self.board)):
            if self.board[i][0] != '-':
                if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                    self.win = True
                    return True
            if self.board[0][i] != '-':
                if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                    self.win = True
                    return True

        if self.board[0][0] != '-':
            if self.board[0][0] == self.board[1][1] == self.board[2][2]:
                self.win = True
                return True

        if self.board[2][0] != '-':
            if self.board[2][0] == self.board[1][1] == self.board[0][2]:
                self.win = True
                return True

    def get_draw(self):
        pieces = 0
        for c in range(len(self.board)):
            for r in range(len(self.board)):
                if self.board[r][c] != '-':
                    pieces += 1

        if pieces == 9:
            return True
        else:
            return False

    def get_legal_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] == '-':
                    moves.append(Move(r, c, self.board))

        return moves

    def make_move(self, move):
        self.move_history.append(move)

        if self.player_1_to_move:
            self.board[move.row][move.col] = 'X'
        else:
            self.board[move.row][move.col] = 'O'

        self.player_1_to_move = not self.player_1_to_move

    def redo_move(self):
        if len(self.move_history) > 0:
            move = self.move_history[-1]
            self.board[move.row][move.col] = '-'
            self.move_history.pop()
            self.player_1_to_move = not self.player_1_to_move


class Move:
    def __init__(self, row, col, board):
        self.row = row
        self.col = col
        self.moveID = row * 10 + col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
