import pygame
import random as rand

width = height = 600

pygame.font.init()
lg_font = pygame.font.SysFont("Micro Sans MS", 60)
sm_font = pygame.font.SysFont("Micro Sans MS", 30)
md_font = pygame.font.SysFont("Micro Sans MS", 40)

try:
    bird = pygame.transform.scale(pygame.image.load(r"FlappyBird\Bird.png"), (65, 50))
except FileNotFoundError:
    bird = pygame.transform.scale(pygame.image.load(r"FlappyBird/Bird.png"), (65, 50))
up_bird = pygame.transform.rotate(bird, 45)
down_bird = pygame.transform.rotate(bird, -45)
try:
    up_pipe = pygame.transform.scale(pygame.image.load(r"FlappyBird\Pipe.png"), (120, 500))
except FileNotFoundError:
    up_pipe = pygame.transform.scale(pygame.image.load(r"FlappyBird/Pipe.png"), (120, 500))
down_pipe = pygame.transform.rotate(up_pipe, 180)

try:
    bg = pygame.transform.scale(pygame.image.load(r"FlappyBird\Background.png"), (600, 600))
except FileNotFoundError:
    bg = pygame.transform.scale(pygame.image.load(r"FlappyBird/Background.png"), (600, 600))


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Oliver\'s Arcade - Flappy Bird")
    clock = pygame.time.Clock()

    bird_x = 200
    bird_y = 250

    pipe_x_1 = 500
    pipe_x_2 = 800
    pipe_x_3 = 1100

    low_pipe_y_1 = rand.randint(100, 430)
    high_pipe_y_1 = low_pipe_y_1 - 570

    low_pipe_y_2 = rand.randint(100, 430)
    high_pipe_y_2 = low_pipe_y_2 - 570

    low_pipe_y_3 = rand.randint(100, 430)
    high_pipe_y_3 = low_pipe_y_3 - 570

    jumping = False
    jumptime = 0

    score = 0
    pause_time = 0

    game_over = False
    game_paused = False

    running = True
    while running:
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        running = False
                        main()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos_x, pos_y = pygame.mouse.get_pos()

                    if 335 > pos_x > 265 and 261 > pos_y > 240:
                        running = False
                        main()
                    elif 350 > pos_x > 260 and 90 > pos_y > 10:
                        running = False

            screen.blit(bg, (0, 0))
            end_screen(screen, score)
            exit_button_go(screen)
            pygame.display.flip()
        elif game_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # pressing esc
                        game_paused = False
                    if event.key == pygame.K_CARET:
                        score = 100
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos_x, pos_y = pygame.mouse.get_pos()

                    if pos_x > width - 47 and pos_y < 65:  # top right pause button
                        game_paused = False
                    if 540 > pos_x > 460 and 65 > pos_y > 15:  # top right exit button
                        running = False

            if pause_time < 2:  # only slightly darkens screen, not fully
                pause_ui(screen)
                pygame.display.flip()
                pause_time += 1
        else:
            pause_time = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        jumping = True
                        jumptime = 0
                    elif event.key == pygame.K_ESCAPE:
                        game_paused = True

            # jumping animation
            if jumping:
                if jumptime <= 5:
                    bird_y -= 9
                    jumptime += 1
                else:
                    jumping = False
                    jumptime = 0
            else:  # falling animation
                bird_y += 9

            # bird off screen
            if bird_y < 1 or bird_y > 560:
                game_over = True

            screen.blit(bg, (0, 0))  # background

            if jumping:  # bird is not falling
                screen.blit(up_bird, (bird_x, bird_y))  # showing the bird tilted up
            else:  # bird is falling
                screen.blit(down_bird, (bird_x, bird_y))  # showing the bird tilted down

            if -120 < pipe_x_1 < 600:
                screen.blit(up_pipe, (pipe_x_1, low_pipe_y_1))  # first batch of pipes
                screen.blit(down_pipe, (pipe_x_1, high_pipe_y_1))

            if -120 < pipe_x_2 < 600:
                screen.blit(up_pipe, (pipe_x_2, low_pipe_y_2))  # second batch of pipes
                screen.blit(down_pipe, (pipe_x_2, high_pipe_y_2))

            if -120 < pipe_x_3 < 600:
                screen.blit(up_pipe, (pipe_x_3, low_pipe_y_3))  # third batch of pipes
                screen.blit(down_pipe, (pipe_x_3, high_pipe_y_3))

            # bird dying
            if (pipe_x_1 + 120 > bird_x + 50 > pipe_x_1 and (bird_y + 40 > low_pipe_y_1 or bird_y < high_pipe_y_1 + 465)) or \
                    (pipe_x_2 + 120 > bird_x + 50 > pipe_x_2 and (bird_y + 40 > low_pipe_y_2 or bird_y < high_pipe_y_2 + 465)) or \
                    (pipe_x_3 + 100 > bird_x + 50 > pipe_x_3 and (bird_y + 40 > low_pipe_y_3 or bird_y < high_pipe_y_3 + 465)):
                game_over = True

            # score
            if pipe_x_1 + 127 > bird_x > pipe_x_1 + 120 or pipe_x_2 + 127 > bird_x > pipe_x_2 + 120 or \
                    pipe_x_3 + 127 > bird_x > pipe_x_3 + 120:
                score += 1

            # moving pipes along the screen
            pipe_x_1 -= 6
            pipe_x_2 -= 6
            pipe_x_3 -= 6

            # resetting pipes x position along the screen
            if pipe_x_1 < -300:
                pipe_x_1 = 600
                low_pipe_y_1 = rand.randint(100, 430)
                high_pipe_y_1 = low_pipe_y_1 - 570

            if pipe_x_2 < -300:
                pipe_x_2 = 600
                low_pipe_y_2 = rand.randint(100, 430)
                high_pipe_y_2 = low_pipe_y_2 - 570

            if pipe_x_3 < -300:
                pipe_x_3 = 600
                low_pipe_y_3 = rand.randint(100, 430)
                high_pipe_y_3 = low_pipe_y_3 - 570

            # showing score
            show_score(screen, score)

            pygame.display.flip()  # updating display

            clock.tick(20)  # capping frame rate to 20fps


def end_screen(screen, score):
    text1 = "Game Over"
    text2 = "Your score was " + str(score)
    text3 = "Restart"

    msg_1 = lg_font.render(text1, False, (255, 0, 0))
    msg_2 = lg_font.render(text2, False, (0, 0, 0))
    r_msg = sm_font.render(text3, False, (60, 60, 60))

    screen.blit(msg_1, (300 - lg_font.size(text1)[0] // 2, 200))
    screen.blit(msg_2, (300 - lg_font.size(text2)[0] // 2, 300))

    screen.blit(r_msg, (300 - sm_font.size(text3)[0] // 2, 240))


def show_score(screen, score):
    text = "Score: " + str(score)

    msg = lg_font.render(text, False, (0, 0, 0))
    screen.blit(msg, (10, 10))


def pause_ui(screen):
    s = pygame.Surface((width, height))
    s.set_alpha(100)
    s.fill((0, 0, 0))
    screen.blit(s, (0, 0))

    pygame.draw.rect(screen, (130, 130, 130), (width - 47, 15, 10, 50))
    pygame.draw.rect(screen, (130, 130, 130), (width - 25, 15, 10, 50))
    exit_button_p(screen)


def exit_button_p(screen):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render('Exit', False, (255, 255, 255))
    pygame.draw.rect(screen, (40, 40, 40), (460, 15, 80, 50))
    screen.blit(text, (470, 15))


def exit_button_go(screen):
    text = md_font.render('Exit', False, (0, 0, 0))
    screen.blit(text, (270, 10))


if __name__ == '__main__':
    main()
