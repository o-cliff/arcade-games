import pygame
import random as rand

width = height = 600
snake_size = 10


def main():
    pygame.init()  # initiating pygame
    screen = pygame.display.set_mode((width, height))  # setting screen dimensions (600, 600)
    pygame.display.set_caption('Oliver\'s Arcade - 2 Player Snake')  # setting pygame caption

    # booleans for recording when a player dies
    game_is_over = False
    game_is_over_2 = False

    # setting a bool for pausing the game
    pause = False

    # starting position of player 1
    x1 = 450
    y1 = 450

    # starting position of player 2
    x2 = 150
    y2 = 150

    # starting direction of player 1
    x_dir = 0
    y_dir = -10

    # starting direction of player 2
    x2_dir = 0
    y2_dir = 10

    # list of snake 1 positions and length of snake 1
    snake_list = []
    snake_len = 3

    # list of snake 2 positions and length of snake 2
    snake_list_2 = []
    snake_len_2 = 3

    # score of snakes
    snake_score = 0
    snake_score_2 = 0

    # starting position of food
    food_x = round(rand.randrange(0, width - snake_size) / 10.0) * 10.0
    food_y = round(rand.randrange(0, height - snake_size) / 10.0) * 10.0

    clock = pygame.time.Clock()  # initiating the clock

    # game loop
    running = True
    while running:
        if game_is_over and game_is_over_2:  # if both players are dead
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
            game_over(screen, snake_score, snake_score_2)
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
                    elif x > 560 and 65 > y:  # top left pause button
                        pause = False

            draw_pause(screen, snake_score, snake_score_2, snake_list, snake_list_2)  # drawing the pause ui
            pygame.draw.rect(screen, (0, 100, 0), (food_x, food_y, 10, 10))  # drawing the food
            pygame.display.flip()

        else:  # if at least one player is alive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # pause button
                    if event.key == pygame.K_ESCAPE:
                        pause = True
                    # changing direction of snake through key presses
                    if event.key == pygame.K_UP:
                        x_dir = 0
                        y_dir = -10
                    if event.key == pygame.K_DOWN:
                        x_dir = 0
                        y_dir = 10
                    if event.key == pygame.K_LEFT:
                        x_dir = -10
                        y_dir = 0
                    if event.key == pygame.K_RIGHT:
                        x_dir = 10
                        y_dir = 0
                    if event.key == pygame.K_w:
                        x2_dir = 0
                        y2_dir = -10
                    if event.key == pygame.K_s:
                        x2_dir = 0
                        y2_dir = 10
                    if event.key == pygame.K_a:
                        x2_dir = -10
                        y2_dir = 0
                    if event.key == pygame.K_d:
                        x2_dir = 10
                        y2_dir = 0

            # filling screen in black
            screen.fill((0, 0, 0))

            # killing the snake if it is dead by removing all the blocks
            if game_is_over:
                snake_len = 0
                snake_list = []
            if game_is_over_2:
                snake_len_2 = 0
                snake_list_2 = []

            if 100 > food_y > 0 and 70 > food_y > 0:  # if the food is in the score view we change the position
                food_y = round(rand.randrange(100, width - snake_size) / 10.0) * 10.0
                food_x = round(rand.randrange(70, height - snake_size) / 10.0) * 10.0

            pygame.draw.rect(screen, (0, 225, 0), (food_x, food_y, 10, 10))  # drawing the food

            if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:  # if player 1 leaves the square
                game_is_over = True
            if x2 >= width or x2 < 0 or y2 >= height or y2 < 0:  # if player 2 leaves the square
                game_is_over_2 = True

            # adding the direction headed to the snake head position
            x1 += x_dir
            y1 += y_dir

            x2 += x2_dir
            y2 += y2_dir

            # setting the snake head position
            snake_head = (x1, y1)

            snake_head_2 = (x2, y2)

            # appending the snake head position to the list of snake positions
            snake_list.append((x1, y1))
            if len(snake_list) > snake_len:
                del snake_list[0]  # deleting first spot of list if it is too long

            # same process for snake 2
            snake_list_2.append((x2, y2))
            if len(snake_list_2) > snake_len_2:
                del snake_list_2[0]

            if snake_head == snake_head_2:  # if snakes collide no extra points are added
                game_is_over = True
                game_is_over_2 = True

            for pos in snake_list[:-1]:  # gets all positions in the list
                if snake_head == pos:  # if the head equals any position (the snake runs into itself)
                    game_is_over = True  # that snake is dead
                if snake_head_2 == pos:  # if the head of snake 2 equals andy position(snake 2 runs into snake 1's head)
                    game_is_over_2 = True  # snake 2 is dead
                    snake_score += 5  # snake 1 gets 5 points

            # same process except reversed for snake 2
            for pos in snake_list_2[:-1]:
                if snake_head_2 == pos:
                    game_is_over_2 = True
                if snake_head == pos:
                    game_is_over = True
                    snake_score_2 += 5

            # drawing the snake in
            draw_snake(screen, snake_list, (255, 0, 0))
            draw_snake(screen, snake_list_2, (0, 0, 255))

            # if the snake head is the same as the food position then a
            # new food position is made and the snake length is increased by one
            if (food_x, food_y) == snake_head and not game_is_over:
                food_x = round(rand.randrange(0, width - snake_size) / 10.0) * 10.0
                food_y = round(rand.randrange(0, height - snake_size) / 10.0) * 10.0
                snake_len += 1
                snake_score += 1
            elif (food_x, food_y) == snake_head_2 and not game_is_over_2:
                food_x = round(rand.randrange(0, width - snake_size) / 10.0) * 10.0
                food_y = round(rand.randrange(0, height - snake_size) / 10.0) * 10.0
                snake_len_2 += 1
                snake_score_2 += 1

            # drawing in the score of the players(the amount of food eaten)
            draw_scores(screen, snake_score, snake_score_2)

            pygame.display.flip()  # updating screen
            clock.tick(30)  # capping fps to 30


def draw_snake(screen, blocks, colour):
    # draws snake by cycling through positions and drawing rectangles to those positions, with appropriate colours
    for pos in blocks:
        pygame.draw.rect(screen, colour, (pos[0], pos[1], 10, 10))


def game_over(screen, score1, score2):
    # draws the game over screen
    game_over_text(screen, score1, score2)
    restart_button(screen)
    exit_button_go(screen)


def game_over_text(screen, score1, score2):
    # draws 'You Died!'
    font = pygame.font.SysFont('Comic Sans MS', 50, italic=True)
    text = font.render('You Died!', False, (0, 255, 0))
    screen.blit(text, (width // 3.4 + 5, height // 4))

    # draws player 1's score
    score_text = font.render('Player 1\'s Score was ' + str(score1), False, (255, 0, 0))
    screen.blit(score_text, (width // 15, height // 2))

    # draws player 2's score
    score_text = font.render('Player 2\'s Score was ' + str(score2), False, (0, 0, 255))
    screen.blit(score_text, (width // 15, height * 0.75))


def restart_button(screen):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render('Restart', False, (130, 130, 130))
    screen.blit(text, (300 - font.size('Restart')[0]//2, 215))


def draw_scores(screen, score1, score2):
    # draws scores while game is active
    font = pygame.font.SysFont('Comic Sans MS', 30, italic=True)
    text1 = font.render('Player 1: ' + str(score1), False, (255, 0, 0))  # player 1
    text2 = font.render('Player 2: ' + str(score2), False, (0, 0, 255))  # player 2

    # blitzes them onto screen
    screen.blit(text1, (0, 0))
    screen.blit(text2, (0, 30))


def exit_button_p(screen):
    # draws exit button
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render('Exit', False, (255, 255, 255))
    pygame.draw.rect(screen, (40, 40, 40), (460, 15, 80, 50))
    screen.blit(text, (470, 15))


def exit_button_go(screen):
    font = pygame.font.SysFont('Comic Sans MS', 40)
    text = font.render('Exit', False, (255, 255, 255))
    screen.blit(text, (270, 10))


def draw_pause(screen, score1, score2, list1, list2):
    screen.fill((30, 30, 30))  # fills screen in grey
    pygame.draw.rect(screen, (130, 130, 130), (width - 47, 15, 10, 50))  # left pause button
    pygame.draw.rect(screen, (130, 130, 130), (width - 25, 15, 10, 50))  # right pause button
    draw_scores(screen, score1, score2)  # score
    draw_snake(screen, list1, (100, 0, 0))  # snake 1
    draw_snake(screen, list2, (0, 0, 100))  # snake 2
    exit_button_p(screen)  # exit button


# calls main function
if __name__ == '__main__':
    main()
