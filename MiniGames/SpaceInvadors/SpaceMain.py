import pygame
import random as rand

width = height = 600
try:
    ship = pygame.image.load(r"SpaceInvadors\goodship.png")
except FileNotFoundError:
    ship = pygame.image.load(r"SpaceInvadors/goodship.png")
ship = pygame.transform.scale(ship, (50, 50))
try:
    ufo = pygame.image.load(r"SpaceInvadors\ufo.png")
except FileNotFoundError:
    ufo = pygame.image.load(r"SpaceInvadors/ufo.png")
ufo = pygame.transform.scale(ufo, (50, 50))

pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 30)


class Bullet:
    def __init__(self, x_pos, y_pos, velocity, colour):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.velocity = velocity
        self.colour = colour


class Enemy:
    def __init__(self, x_pos, y_pos, velocity, image, screen):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.vel = velocity
        self.image = image
        self.screen = screen
        self.collidepoint = self.screen.blit(self.image, (self.x_pos, self.y_pos))

    def show(self):
        self.collidepoint = self.screen.blit(self.image, (self.x_pos, self.y_pos))


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Oliver\'s Arcade - Space Invaders')
    clock = pygame.time.Clock()

    y = height - 80
    x = width // 2 - 25
    i = 0

    game_over = False
    game_paused = False

    move_right = False
    move_left = False

    bullets = []
    enemies = []
    rand_nums = [4]

    score = 0
    lives = 3
    can_shoot = True
    last_shot = 0

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
            game_over_display(screen, score)
            pygame.display.flip()

        elif game_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # pause button
                        game_paused = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x1, y1 = pygame.mouse.get_pos()
                    if 540 > x1 > 460 and 65 > y1 > 15:  # top right exit button
                        running = False
                    elif x1 > 560 and 65 > y1:  # top left pause button
                        game_paused = False

            # removing all movements to stop them continuing when press resume
            move_left = False
            move_right = False

            # drawing the pause ui
            draw_pause(screen, score, lives)
            for enemy in enemies:
                enemy.show()
            for bullet in bullets:
                pygame.draw.rect(screen, bullet.colour, (bullet.x_pos, bullet.y_pos, 10, 20))
            screen.blit(ship, (x, y))
            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move_left = True
                    if event.key == pygame.K_RIGHT:
                        move_right = True
                    if event.key == pygame.K_UP:
                        if can_shoot:
                            bullets.append(Bullet(x + 20, y, 12, (0, 255, 0)))
                            can_shoot = False
                            last_shot = 0
                    if event.key == pygame.K_ESCAPE:
                        game_paused = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        move_left = False
                    if event.key == pygame.K_RIGHT:
                        move_right = False

            screen.fill((0, 0, 0))

            if last_shot > 45:
                can_shoot = True

            last_shot += 1

            if move_right:
                x += 4
                if x > width - 50:
                    x -= 4
            if move_left:
                x -= 4
                if x < 0:
                    x += 4

            for bullet in bullets:
                if bullet.y_pos < 0:
                    bullets.remove(bullet)
                else:
                    pygame.draw.rect(screen, bullet.colour, (bullet.x_pos, bullet.y_pos, 10, 20))
                    bullet.y_pos -= bullet.velocity

            for num in rand_nums:
                if num == rand.randint(0, 10000) or i == 0 or i > 200:
                    i = 1
                    rand_nums.append(rand.randint(0, 10000))
                    enemies.append(Enemy(rand.randint(60, width - 60), 70, rand.choice([8, -8, 4, -4]), ufo, screen))

            i += 1

            for enemy in enemies:
                for bullet in bullets:
                    if bullet.colour == (0, 255, 0):
                        pos = (bullet.x_pos, bullet.y_pos)
                        if enemy.x_pos + 50 >= pos[0] >= enemy.x_pos and enemy.y_pos + 50 >= pos[1] >= enemy.y_pos:
                            enemies.remove(enemy)
                            bullets.remove(bullet)
                if enemy.y_pos == y:
                    lives -= 1
                    enemies.remove(enemy)
                if enemy.x_pos <= 0 or enemy.x_pos >= width - 50:
                    enemy.y_pos += 50
                    enemy.vel = -1 * enemy.vel
                    enemy.x_pos += enemy.vel
                else:
                    enemy.show()
                    enemy.x_pos += enemy.vel
                    if rand.randint(0, 200) == rand.randint(0, 200):
                        bullets.append(Bullet(enemy.x_pos + 20, enemy.y_pos, -12, (255, 0, 0)))

            for bullet in bullets:
                if bullet.colour == (255, 0, 0):
                    pos = (bullet.x_pos, bullet.y_pos)
                    if x + 50 >= pos[0] >= x and y + 50 >= pos[1] >= y:
                        lives -= 1
                        bullets.remove(bullet)

            screen.blit(ship, (x, y))

            score += 1

            if lives <= 0:
                game_over = True

            show_score(screen, score)
            show_lives(screen, lives)

            pygame.display.flip()
            clock.tick(60)


def show_score(screen, score):
    text = font.render('Score: ' + str(score // 2), False, (255, 255, 255))
    screen.blit(text, (10, 10))


def show_lives(screen, lives):
    text = font.render('Lives: ' + str(lives), False, (255, 255, 255))
    screen.blit(text, (10, 40))


def game_over_display(screen, score):
    game_over_text(screen, score)
    restart_button(screen)
    exit_button_go(screen)


def game_over_text(screen, score):
    # draws 'You Died!'
    font1 = pygame.font.SysFont('Comic Sans MS', 50, italic=True)
    text = font1.render('You Died!', False, (0, 255, 0))
    screen.blit(text, (width // 2 - font1.size('You Died!')[0] // 2, height // 4))

    # draws player 1's score
    score_text = font1.render('Your score was ' + str(score // 2), False, (255, 0, 0))
    screen.blit(score_text, (width // 7, height // 2))


def restart_button(screen):
    text = font.render('Restart', False, (130, 130, 130))
    screen.blit(text, (300 - font.size('Restart')[0]//2, 215))


def exit_button_p(screen):
    font1 = pygame.font.SysFont('Comic Sans MS', 30)
    text = font1.render('Exit', False, (255, 255, 255))
    pygame.draw.rect(screen, (40, 40, 40), (460, 15, 80, 50))
    screen.blit(text, (470, 15))


def exit_button_go(screen):
    font1 = pygame.font.SysFont('Comic Sans MS', 40)
    text = font1.render('Exit', False, (255, 255, 255))
    screen.blit(text, (270, 10))


def draw_pause(screen, score, lives):
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (130, 130, 130), (width - 47, 15, 10, 50))
    pygame.draw.rect(screen, (130, 130, 130), (width - 25, 15, 10, 50))
    show_score(screen, score)
    show_lives(screen, lives)
    exit_button_p(screen)


if __name__ == '__main__':
    main()
