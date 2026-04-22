import pygame

width = height = 600


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Oliver\'s Arcade - Pong")

    player_1_y = 275
    player_1_up = False
    player_1_down = False

    player_2_y = 275
    player_2_up = False
    player_2_down = False

    ball_x = 300
    ball_y = 5
    ball_vel_x = 3
    ball_vel_y = 3

    player_1_score = 0
    player_2_score = 0

    game_over = False
    game_paused = False

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

            screen.fill((0, 0, 0))

            game_over_(screen, player_1_score, player_2_score)
            pygame.display.flip()

        elif game_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 540 > x > 460 and 65 > y > 15:
                        running = False
                    elif x > 560 and 65 > y:
                        game_paused = False

            screen.fill((60, 60, 60))
            draw_pause(screen, player_1_score, player_2_score, player_1_y, player_2_y, ball_x, ball_y)
            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = True
                    if event.key == pygame.K_UP:
                        player_2_up = True
                    if event.key == pygame.K_DOWN:
                        player_2_down = True
                    if event.key == pygame.K_w:
                        player_1_up = True
                    if event.key == pygame.K_s:
                        player_1_down = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        player_2_up = False
                    if event.key == pygame.K_DOWN:
                        player_2_down = False
                    if event.key == pygame.K_w:
                        player_1_up = False
                    if event.key == pygame.K_s:
                        player_1_down = False

            if player_1_up and player_1_y > 3:
                player_1_y -= 4
            if player_1_down and player_1_y < 547:
                player_1_y += 4
            if player_2_up and player_2_y > 3:
                player_2_y -= 4
            if player_2_down and player_2_y < 547:
                player_2_y += 4

            if ball_y <= 0 or ball_y >= 594:
                ball_vel_y *= -1

            if (589 > ball_x > 579 and 50 + player_2_y > ball_y > player_2_y) or \
                    (1 < ball_x < 11 and 50 + player_1_y > ball_y > player_1_y):
                ball_vel_x *= -1
                if ball_y - player_2_y > -25:
                    ball_vel_y -= 0.3
                else:
                    ball_vel_y += 0.3
            elif (589 > ball_x + 10 > 579 and 50 + player_2_y > ball_y + 10 > player_2_y) or \
                    (1 < ball_x + 10 < 11 and 50 + player_1_y > ball_y + 10 > player_1_y):
                ball_vel_x *= -1
                if ball_y - player_2_y > -25:
                    ball_vel_y -= 0.3
                else:
                    ball_vel_y += 0.3
            elif (589 > ball_x + 10 > 579 and 50 + player_2_y > ball_y > player_2_y) or \
                    (1 < ball_x + 10 < 11 and 50 + player_1_y > ball_y > player_1_y):
                ball_vel_x *= -1
                if ball_y - player_2_y > -25:
                    ball_vel_y -= 0.3
                else:
                    ball_vel_y += 0.3
            elif (589 > ball_x > 579 and 50 + player_2_y > ball_y + 10 > player_2_y) or \
                    (1 < ball_x < 11 and 50 + player_1_y > ball_y + 10 > player_1_y):
                ball_vel_x *= -1
                if ball_y - player_2_y > -25:
                    ball_vel_y -= 0.3
                else:
                    ball_vel_y += 0.3

            elif 0 > ball_x:
                player_2_score += 1
                ball_x = 300
                ball_y = 1
                ball_vel_x = 2.5
                ball_vel_y = 2
            elif 590 < ball_x:
                player_1_score += 1
                ball_x = 300
                ball_y = 1
                ball_vel_x = 2.5
                ball_vel_y = 2.5

            ball_y += ball_vel_y
            ball_x += ball_vel_x

            if ball_vel_x > 0:
                ball_vel_x += 0.01
            else:
                ball_vel_x -= 0.01

            screen.fill((0, 0, 0))

            draw_chars(screen, player_1_y, player_2_y)
            draw_scores(screen, player_1_score, player_2_score)
            draw_ball(screen, ball_x, ball_y)

            pygame.display.flip()
            clock.tick(60)

            if player_1_score == 5 or player_2_score == 5:
                game_over = True


def draw_chars(screen, y_1, y_2):
    pygame.draw.rect(screen, (255, 255, 255), (5, y_1, 5, 50))
    pygame.draw.rect(screen, (255, 255, 255), (590, y_2, 5, 50))


def draw_ball(screen, x, y):
    pygame.draw.rect(screen, (0, 255, 0), (x, y, 10, 10))


def draw_scores(screen, score1, score2):
    font = pygame.font.SysFont('Micro Sans MS', 30)
    text = font.render(str(score1) + ' | ' + str(score2), False, (255, 255, 255))

    screen.blit(text, (300 - 30 // 2, 10))


def game_over_(screen, score1, score2):
    # draws the game over screen
    game_over_text(screen, score1, score2)
    restart_button(screen)
    exit_button_go(screen)


def game_over_text(screen, score1, score2):
    # draws 'You Died!'
    font = pygame.font.SysFont('Comic Sans MS', 50, italic=True)
    if score1 > score2:
        text = font.render('Player 1 Wins', False, (0, 255, 0))
    else:
        text = font.render('Player 2 Wins', False, (0, 255, 0))

    screen.blit(text, (width // 4, height // 4))

    # draws player 1's score
    score_text = font.render('Player 1\'s Score was ' + str(score1), False, (255, 0, 0))
    screen.blit(score_text, (width // 15, height // 2))

    # draws player 2's score
    score_text = font.render('Player 2\'s Score was ' + str(score2), False, (0, 0, 255))
    screen.blit(score_text, (width // 15, height * 0.75))


def restart_button(screen):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render('Restart', False, (130, 130, 130))
    screen.blit(text, (width//2 - (font.size('Restart')[0])//2, 215))


def exit_button_p(screen):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render('Exit', False, (255, 255, 255))
    pygame.draw.rect(screen, (40, 40, 40), (460, 15, 80, 50))
    screen.blit(text, (470, 15))


def exit_button_go(screen):
    font = pygame.font.SysFont('Comic Sans MS', 40)
    text = font.render('Exit', False, (255, 255, 255))
    screen.blit(text, (270, 10))


def draw_pause(screen, score1, score2, y1, y2, x, y):
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (130, 130, 130), (width - 47, 15, 10, 50))
    pygame.draw.rect(screen, (130, 130, 130), (width - 25, 15, 10, 50))
    draw_scores(screen, score1, score2)
    draw_chars(screen, y1, y2)
    exit_button_p(screen)
    draw_ball(screen, x, y)


if __name__ == '__main__':
    main()
