import pygame
from ChessEngine2 import ChessEngine
from ChessEngine2 import MiniMax
from ChessEngine2 import OpeningBook
from Errors import s1And0s as e1

width = height = 600  # 800 is too large
dimension = 8  # dimension of a chess board
square_size = height // dimension
max_fps = 15
images = {}
colours = []


def load_images():
    # load images into global dictionary
    pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk', 'bp', 'br', 'bn', 'bb', 'bq', 'bk']

    for piece in pieces:
        images[piece] = \
            pygame.transform.scale(pygame.image.load(
                r"ChessEngine2\128px\{}.png".format(piece)),
                (square_size, square_size))


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Oliver\'s Arcade - Chess")
    clock = pygame.time.Clock()
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    animate = False  # for move animations

    load_images()
    square_selected = ()
    player_clicks = []

    game_over = False
    result = 0

    running = True
    while running:
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        gs.undo_move(notation=True)
                        gs.undo_move()
                        animate = False
                        move_made = True
                    if event.key == pygame.K_r:
                        gs = ChessEngine.GameState()
                        valid_moves = gs.get_valid_moves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            draw_game_over(screen, gs.board, result)

            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and gs.white_to_move:
                    location = pygame.mouse.get_pos()
                    col = location[0] // square_size
                    row = location[1] // square_size
                    if square_selected == (row, col):
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)
                    if len(player_clicks) == 2:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i], notation=True)
                                animate = True
                                move_made = True
                                square_selected = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        gs.undo_move(notation=True)
                        gs.undo_move()
                        animate = False
                        move_made = True
                    if event.key == pygame.K_r:
                        gs = ChessEngine.GameState()
                        valid_moves = gs.get_valid_moves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif not gs.white_to_move:
                    pos = OpeningBook.BlackOpeningBook(gs)
                    if pos.move != ():
                        move = ChessEngine.Move(pos.move[0], pos.move[1], gs.board)
                        move_made = True
                        animate = True
                        gs.make_move(move, notation=True)
                    elif pos.move == ():
                        temp_castle = (gs.castle_rights.wks, gs.castle_rights.bks,
                                       gs.castle_rights.wqs, gs.castle_rights.bqs)
                        temp_castle_log = gs.castle_rights_log
                        move = MiniMax.minimax_root(3, gs, True)
                        gs.castle_rights = ChessEngine.CastleRights(temp_castle[0], temp_castle[1],
                                                                    temp_castle[2], temp_castle[3])
                        gs.castle_rights_log = temp_castle_log
                        if move:
                            animate = True
                            move_made = True
                            square_selected = ()
                            player_clicks = []
                            gs.make_move(move, notation=True)
                        else:
                            if gs.square_under_attack(gs.black_king_location[0], gs.black_king_location[1]):
                                game_over = True
                                e1.main()
                                running = False
            if move_made:
                if animate:
                    animate_move(gs.move_history[-1], screen, gs.board, clock)
                valid_moves = gs.get_valid_moves()
                move_made = False
                animate = False
                if len(valid_moves) == 0:
                    if gs.square_under_attack(gs.white_king_location[0], gs.white_king_location[1]):
                        game_over = True
                        result = 1

            draw_game_state(screen, gs, valid_moves, square_selected)

            clock.tick(max_fps)
            pygame.display.flip()


def draw_highlights_squares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):  # selects moveable piece
            s = pygame.Surface((square_size, square_size))
            s.set_alpha(100)  # transparency value
            s.fill((40, 255, 60))
            screen.blit(s, (c * square_size, r * square_size))
            s.fill((200, 200, 0))
            for move in valid_moves:
                if (move.start_row, move.start_col) == (r, c):
                    screen.blit(s, (move.end_col * square_size, move.end_row * square_size))


def draw_game_state(screen, gs, valid_moves, sq_selected):
    # drawing the board and pieces
    draw_board(screen)
    draw_highlights_squares(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    global colours
    # drawing a 8x8 board into pygame
    colours = [(222, 184, 135), (133, 96, 66)]

    for i in range(dimension):
        for j in range(dimension):
            rect = pygame.Rect(j * square_size, i * square_size, square_size, square_size)
            colour = colours[((i+j) % 2)]
            pygame.draw.rect(screen, colour, rect)


def draw_pieces(screen, board):
    # drawing the pieces and their position into pygame
    for i in range(dimension):
        for j in range(dimension):
            rect = pygame.Rect(i * square_size, j * square_size, square_size, square_size)
            piece = board[j][i]
            if piece != '--':
                screen.blit(images[piece], rect)


def animate_move(move, screen, board, clock):
    global colours
    d_r = move.end_row - move.start_row
    d_c = move.end_col - move.start_col
    frames_per_square = 5  # frames to move 1 square
    frame_count = (abs(d_r) + abs(d_c)) * frames_per_square

    for frame in range(frame_count + 1):
        r, c = (move.start_row + d_r*frame/frame_count, move.start_col + d_c*frame/frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        colour = colours[(move.end_row + move.end_col) % 2]
        end_square = pygame.Rect(move.end_col*square_size, move.end_row *
                                 square_size, square_size, square_size)
        pygame.draw.rect(screen, colour, end_square)

        #  draw captured piece onto square
        if move.piece_captured != '--':
            screen.blit(images[move.piece_captured], end_square)

        #  draw moving piece
        screen.blit(images[move.piece_moved], (c*square_size,
                                               r*square_size, square_size, square_size))
        pygame.display.flip()
        clock.tick(60)


def draw_red_tint(screen):
    s = pygame.Surface((width, height))
    s.set_alpha(150)
    s.fill((50, 0, 0))
    screen.blit(s, (0, 0))


def draw_game_over(screen, board, result):
    draw_board(screen)
    draw_pieces(screen, board)
    draw_red_tint(screen)
    draw_text(screen, result)


def draw_text(screen, result):
    col = {"You Lose": (255, 0, 0), "It's a Draw!": (0, 0, 255)}
    font = pygame.font.SysFont("Micro Sans MS", 60, bold=True)
    text1 = "You Lose" if result == 1 else "It's a Draw!"
    text = font.render(text1, False, col[text1])
    screen.blit(text, (300 - font.size(text1)[0] // 2, 300 - font.size(text1)[1] // 2))


if __name__ == '__main__':
    main()
