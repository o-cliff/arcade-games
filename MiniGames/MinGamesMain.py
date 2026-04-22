from SnakeGame1Player import SnakeGameMain as sgm  # 1
from SnakeGame2Player import SnakeGame2PlayerMain as sg2m  # 2
from ChessEngine2 import ChessMain as cm  # c
from NoughtsAndCrosses import Main as ncm  # t
from Pong import PongMain as pm  # p
from SpaceInvadors import SpaceMain as sm  # s
from FlappyBird import BirdMain as bm  # b
import pygame

pygame.font.init()
font = pygame.font.SysFont("Micro Sans MS", 22)
small_font = pygame.font.SysFont("Micro Sans MS", 30)
large_font = pygame.font.SysFont("Micro Sans MS", 60)

try:    # this is to ensure it works on both linux and windows environments, follows for all image
        # calls. It  happens because the file structure works with '/' on linux but '\' on windows
    logo = pygame.image.load(
        r"Images\logo.jpg")
except FileNotFoundError:
    logo = pygame.image.load(
        r"Images/logo.jpg")

images = []

games = {'1 Player Snake Game': '1', '2 Player Snake Game': '2', 'Chess': 'c', 'Tic Tac Toe': 't',
         'Pong': 'p', 'Space Invaders': 's', 'Flappy Bird': 'b'}
names = ['1 Player Snake Game', '2 Player Snake Game',
         'Chess', 'Tic Tac Toe', 'Pong', 'Space Invaders', 'Flappy Bird']
colours = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (128, 0, 128),
           (255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (128, 0, 128)]
mains = [sgm, sg2m, cm, ncm, pm, sm, bm]


def load_images():
    try:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images\SnakeGame1Player.jpg"), (300, 300)))
    except FileNotFoundError:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images/SnakeGame1Player.jpg"), (300, 300)))

    try:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images\SnakeGame2Player.jpg"), (300, 300)))
    except FileNotFoundError:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images/SnakeGame2Player.jpg"), (300, 300)))

    try:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images\Chess.jpg"), (300, 300)))
    except FileNotFoundError:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images/Chess.jpg"), (300, 300)))

    try:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images\TicTacToe.jpg"), (300, 300)))
    except FileNotFoundError:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images/TicTacToe.jpg"), (300, 300)))

    try:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images\Pong.jpg"), (300, 300)))
    except FileNotFoundError:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images/Pong.jpg"), (300, 300)))

    try:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images\SpaceInvaders.jpg"), (300, 300)))
    except FileNotFoundError:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images/SpaceInvaders.jpg"), (300, 300)))

    try:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images\FlappyBird.jpg"), (300, 300)))
    except FileNotFoundError:
        images.append(
            pygame.transform.scale(pygame.image.load(r"Images/FlappyBird.jpg"), (300, 300)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Oliver\'s Arcade')
    pygame.display.set_icon(logo)
    image_num = 0
    load_images()
    show_left_sidebar = False
    show_right_sidebar = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # chess
                    cm.main()
                    screen = pygame.display.set_mode((600, 600))
                elif event.key == pygame.K_1:  # one player snake game
                    sgm.main()
                elif event.key == pygame.K_2:  # two player snake game
                    sg2m.main()
                elif event.key == pygame.K_s:  # space invaders
                    sm.main()
                elif event.key == pygame.K_t:  # tic tac toe
                    ncm.main()
                    screen = pygame.display.set_mode((600, 600))
                elif event.key == pygame.K_p:  # pong
                    pm.main()
                elif event.key == pygame.K_b:  # flappy bird
                    bm.main()
                elif event.key == pygame.K_LEFT:  # changing image to the left
                    if image_num == 0:
                        image_num = 6
                    else:
                        image_num -= 1
                elif event.key == pygame.K_RIGHT:  # changing image to the right
                    if image_num == 6:
                        image_num = 0
                    else:
                        image_num += 1
                elif event.key == pygame.K_RETURN:  # selecting image by pressing enter
                    mains[image_num].main()
                    screen = pygame.display.set_mode((600, 600))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posx, posy = pygame.mouse.get_pos()
                if 140 > posx > 100 and 410 > posy > 90:  # changing image to the left
                    if image_num == 0:
                        image_num = 6
                    else:
                        image_num -= 1
                elif 500 > posx > 460 and 410 > posy > 90:  # changing image to the right
                    if image_num == 6:
                        image_num = 0
                    else:
                        image_num += 1
                elif 460 > posx > 140 and 410 > posy > 90:  # selecting game by clicking on image
                    mains[image_num].main()
                    screen = pygame.display.set_mode((600, 600))
            elif event.type == pygame.MOUSEMOTION:
                posx, posy = pygame.mouse.get_pos()
                if 200 > posx > 100 and 410 > posy > 90:  # left quarter
                    show_left_sidebar = True
                else:
                    show_left_sidebar = False

                if 500 > posx > 400 and 410 > posy > 90:  # right quarter
                    show_right_sidebar = True
                else:
                    show_right_sidebar = False

        pygame.display.set_caption('Oliver\'s Arcade')
        intro(screen, image_num)
        main_image(screen, image_num)

        if show_right_sidebar:
            right_sidebar(screen)
        if show_left_sidebar:
            left_sidebar(screen)

        pygame.display.flip()


def intro(screen, num):
    screen.fill((0, 0, 0))
    intro_text = large_font.render("Welcome to Oliver\'s Arcade!", False, (255, 255, 255))
    screen.blit(intro_text, (300 - large_font.size("Welcome to Oliver\'s Arcade!")[0] // 2, 10))
    y = 420
    col = 0
    for game in names:
        msg = "Press \"" + games[game] + "\" to play " + game
        text = font.render(msg, False, colours[col])
        if col == num and col < 6:
            pygame.draw.rect(screen, (40, 40, 40), (149 - font.size(msg)
                                                    [0] // 2, y - 1, font.size(msg)[0] + 2, font.size(msg)[1] + 2))
        elif col == num and col >= 6:
            pygame.draw.rect(screen, (40, 40, 40), (449 - font.size(msg)
                                                    [0] // 2, y - 181, font.size(msg)[0] + 2, font.size(msg)[1] + 2))
        if col < 6:
            screen.blit(text, (150 - font.size(msg)[0] // 2, y))
        else:
            screen.blit(text, (450 - font.size(msg)[0] // 2, y - 180))

        y += 30
        col += 1


def main_image(screen, num):
    text = small_font.render(names[num], False, colours[num])
    image = images[num]
    pygame.draw.rect(screen, colours[num], (140, 90, 320, 320))
    screen.blit(image, (150, 100))
    screen.blit(text, (300 - small_font.size(names[num])[0] // 2, 60))


def left_sidebar(screen):
    pygame.draw.rect(screen, (40, 40, 40), (100, 90, 40, 320))
    pygame.draw.polygon(screen, (0, 0, 0), ((103, 250), (133, 280), (133, 220)))


def right_sidebar(screen):
    pygame.draw.rect(screen, (40, 40, 40), (460, 90, 40, 320))
    pygame.draw.polygon(screen, (0, 0, 0), ((497, 250), (467, 280), (467, 220)))


if __name__ == '__main__':
    main()
