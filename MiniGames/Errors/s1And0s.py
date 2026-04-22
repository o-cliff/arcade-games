import random as rand
import pygame

width = height = 600
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 10)
rand_cap = str(rand.randint(0, 1))
for numeral_that_has_a_name in range(0, 20):
    rand_cap = rand_cap + str(rand.randint(0, 1))


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(rand_cap)
    screen.fill((255, 255, 255))
    r = 0
    c = 0
    i = 0

    locations = [(0, 0)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        if c < 600:
            r += 10
            if r >= width:
                r = 0
                c += 10
            locations.append((r, c))
        else:
            i += 1

            if i >= 15:
                break

            print_msg(screen, locations)

            pygame.display.flip()


def print_msg(screen, locations):
    for loc in locations:
        num = rand.randint(0, 1)
        text = font.render(str(num), False, (255, 255, 255))
        screen.blit(text, loc)


if __name__ == "__main__":
    main()
