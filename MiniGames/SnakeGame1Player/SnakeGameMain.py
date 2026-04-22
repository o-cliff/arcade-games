import pygame
import random as rand

width = height = 600


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Oliver\'s Arcade - Snake")
    clock = pygame.time.Clock()

    x_dir = 0
    y_dir = -10

    x_pos = 300
    y_pos = 300

    snake_list = []
    snake_len = 3
    snake_score = 0

    food_pos_x = rand.randint(0, 60) * 10
    food_pos_y = rand.randint(0, 60) * 10

    game_over = False
    pause = False

    running = True
    while running:
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                    if 254 > mouse_pos_y > 230 and 350 > mouse_pos_x > 250:
                        running = False
                        main()
                    elif 350 > mouse_pos_x > 260 and 90 > mouse_pos_y > 10:
                        running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        screen.fill((0, 0, 0))
                        pygame.display.flip()
                        running = False
                        main()

            # show end screen
            screen.fill((0, 0, 0))
            game_over_display(screen, snake_score)
            pygame.display.flip()

        elif pause:  # if game is paused
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # pause button
                        pause = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 540 > x > 460 and 65 > y > 15:  # top right exit button
                        running = False
                    elif x > 560 and 65 > y:  # top right pause button
                        pause = False

            draw_pause(screen, snake_score, snake_list)  # drawing the pause ui
            pygame.draw.rect(screen, (0, 100, 0), (food_pos_x, food_pos_y, 10, 10))  # drawing the food
            pygame.display.flip()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        x_dir = 0
                        y_dir = -10
                    if event.key == pygame.K_DOWN:
                        x_dir = 0
                        y_dir = 10
                    elif event.key == pygame.K_LEFT:
                        x_dir = -10
                        y_dir = 0
                    elif event.key == pygame.K_RIGHT:
                        x_dir = 10
                        y_dir = 0
                    elif event.key == pygame.K_ESCAPE:
                        pause = True

            screen.fill((0, 0, 0))

            pygame.draw.rect(screen, (0, 255, 0), (food_pos_x, food_pos_y, 10, 10))

            x_pos += x_dir
            y_pos += y_dir

            head = (x_pos, y_pos)

            if 600 <= x_pos or 0 > x_pos or 600 <= y_pos or 0 > y_pos:
                game_over = True

            snake_list.append(head)

            if len(snake_list) > snake_len:
                del snake_list[0]

            for pos in snake_list[:-1]:
                if head == pos:
                    game_over = True

            draw_snakes(screen, snake_list, (0, 0, 255))
            draw_score(screen, snake_score)

            pygame.display.flip()

            if head == (food_pos_x, food_pos_y):
                food_pos_x = rand.randint(0, 59) * 10
                food_pos_y = rand.randint(0, 59) * 10
                snake_len += 1
                snake_score += 1

            clock.tick(30)


def draw_snakes(screen, posses, colour):
    for pos in posses:
        pygame.draw.rect(screen, colour, (pos[0], pos[1], 10, 10))


def draw_score(screen, score):
    font = pygame.font.SysFont("Comic Sans MS", 30)
    text = font.render("Score: " + str(score), False, (255, 0, 0))

    screen.blit(text, (2, 2))


def game_over_display(screen, score):
    game_over_text(screen, score)
    restart_button(screen)
    exit_button_go(screen)


def game_over_text(screen, score):
    # draws 'You Died!'
    font = pygame.font.SysFont('Comic Sans MS', 50, italic=True)
    text = font.render('You Died!', False, (0, 255, 0))
    screen.blit(text, (width // 3.4 + 5, height // 4))

    # draws player 1's score
    score_text = font.render('Your score was ' + str(score), False, (255, 0, 0))
    screen.blit(score_text, (width // 7, height // 2))


def restart_button(screen):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render('Restart', False, (130, 130, 130))
    screen.blit(text, (300 - font.size('Restart')[0]//2, 215))


def exit_button_p(screen):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render('Exit', False, (255, 255, 255))
    pygame.draw.rect(screen, (40, 40, 40), (460, 15, 80, 50))
    screen.blit(text, (470, 15))


def exit_button_go(screen):
    font = pygame.font.SysFont('Comic Sans MS', 40)
    text = font.render('Exit', False, (255, 255, 255))
    screen.blit(text, (270, 10))


def draw_pause(screen, score, list1):
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (130, 130, 130), (width - 47, 15, 10, 50))
    pygame.draw.rect(screen, (130, 130, 130), (width - 25, 15, 10, 50))
    draw_score(screen, score)
    draw_snakes(screen, list1, (0, 0, 100))
    exit_button_p(screen)


if __name__ == '__main__':
    main()
