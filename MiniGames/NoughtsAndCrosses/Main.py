import pygame
import sys
sys.path.append(r'C:\Users\45665\Desktop\Schoolwork\Coding\Python\MiniGames\NoughtsAndCrosses')
from NoughtsAndCrosses import Engine as e

width = height = 400  # 800 is too large
dimension = 3  # dimension of a chess board
square_size = height // dimension
max_fps = 15
first_move = True


def main():
    global first_move
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Oliver\'s Arcade - Tic Tac Toe')
    gs = e.GameState()
    game_over = False
    restart = False

    if not first_move:
        gs.player_1_to_move = False

    running = True
    while running:
        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and gs.player_1_to_move:
                    mouse_pos = pygame.mouse.get_pos()

                    x, y = mouse_pos
                    row = x // square_size
                    col = y // square_size

                    move = e.Move(row, col, gs.board)

                    if move in gs.get_legal_moves():
                        gs.make_move(move)
                        gs.player_1_to_move = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        gs.redo_move()
                        gs.redo_move()
                        gs.player_1_to_move = True
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            if gs.get_win() or gs.get_draw():
                draw_game_state(gs.board, screen)
                pygame.display.flip()
                game_over = True
            else:
                draw_game_state(gs.board, screen)
                pygame.display.flip()

                if not gs.player_1_to_move:
                    (m, px, py) = max_alpha_beta(gs, -2, 2)
                    move = e.Move(px, py, gs.board)
                    gs.player_1_to_move = False
                    gs.make_move(move)
                    gs.player_1_to_move = True

        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    x, y = mouse_pos

                    if 300 > y > 200 and 350 > x > 50:
                        restart = True
                        running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            if gs.get_win():
                win(not gs.player_1_to_move, screen, gs)
            else:
                draw(screen, gs)
            pygame.display.flip()

    if restart:
        first_move = not first_move
        main()


def draw_game_state(board, screen):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, height))
    draw_board(board, screen)
    draw_piece(board, screen)


def draw_board(board, screen):
    for c in range(len(board)):
        for r in range(len(board[c])):
            rect = pygame.Rect(r * (square_size + 1), c * (square_size + 1), square_size, square_size)

            pygame.draw.rect(screen, (255, 255, 255), rect)


def draw_piece(board, screen):
    for c in range(len(board)):
        for r in range(len(board[c])):
            colours = {'X': (255, 0, 0), 'O': (0, 0, 255), '-': (0, 0, 0)}
            my_font = pygame.font.SysFont('Comic Sans MS', square_size)
            text = my_font.render(str(board[r][c]), False, colours[board[r][c]])

            screen.blit(text, (r * square_size, c * square_size - square_size//4))


def win(player_turn, screen, gs):
    pygame.draw.rect(screen, (55, 0, 0), (0, 0, width, height))
    draw_piece(gs.board, screen)
    win_text(player_turn, screen)
    win_button(screen)


def draw(screen, gs):
    pygame.draw.rect(screen, (0, 255, 0), (0, 0, width, height))
    draw_piece(gs.board, screen)
    draw_text(screen)
    win_button(screen)


def draw_text(screen):
    myfont = pygame.font.SysFont('Comic Sans MS', width // 8, italic=True)
    text = myfont.render('It\'s a draw', False, (0, 60, 0))
    screen.blit(text, (height // 4 - 20, width // 4))


def win_text(player_turn, screen):
    myfont = pygame.font.SysFont('Comic Sans MS', width // 8, italic=True)
    if player_turn:
        text = myfont.render('You Win', False, (0, 0, 0))
    else:
        text = myfont.render('You Lose', False, (255, 155, 0))

    screen.blit(text, (height // 4, width // 4))


def win_button(screen):
    pygame.draw.rect(screen, (0, 0, 0), (50, 200, 300, 100))  # rectangle around restart

    # restart text
    my_font = pygame.font.SysFont('Comic Sans MS', width // 8)
    text = my_font.render('Restart', False, (255, 0, 0))
    screen.blit(text, (100, 210))


def evaluation(gs):
    if gs.get_win() and gs.player_1_to_move:
        return 1
    elif gs.get_win() and not gs.player_1_to_move:
        return -1
    elif gs.get_draw():
        return 0


def max_alpha_beta(gs, alpha, beta):
    max_v = -2
    px = None
    py = None

    if gs.get_win() or gs.get_draw():
        return (evaluation(gs), 0, 0)

    for move in gs.get_legal_moves():
        gs.make_move(move)
        m, min_i, in_j = min_alpha_beta(gs, alpha, beta)
        if m > max_v:
            max_v = m
            px, py = move.row, move.col
        gs.redo_move()

        if max_v >= beta:
            return (max_v, px, py)
        if max_v > alpha:
            alpha = max_v

    return (max_v, px, py)


def min_alpha_beta(gs, alpha, beta):
    minv = 2

    qx = None
    qy = None

    if gs.get_win() or gs.get_draw():
        return (evaluation(gs), 0, 0)

    for move in gs.get_legal_moves():
        gs.make_move(move)
        m, max_i, max_j = max_alpha_beta(gs, alpha, beta)

        if m < minv:
            minv = m
            qx, qy = move.row, move.col
        gs.redo_move()

        if minv <= alpha:
            return (minv, qx, qy)
        if minv < beta:
            beta = minv

    return (minv, qx, qy)


if __name__ == '__main__':
    main()
