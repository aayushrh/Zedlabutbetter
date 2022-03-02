import sys
import pygame
from pygame import K_w, K_a, K_s, K_d
pygame.init()

fps = 60
clock = pygame.time.Clock()
width, height = 256, 160
true_screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
screen = pygame.Surface((width, height))
tile_size = 16

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
        self.walk_cooldown_max = 10
        self.walk_cooldown = 0

    def draw(self, s):
        s.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.walk_cooldown -= 1
        keys = pygame.key.get_pressed()
        if self.walk_cooldown <= 0:
            if keys[K_w]:
                self.rect.y -= tile_size
                self.walk_cooldown = self.walk_cooldown_max
            elif keys[K_s]:
                self.rect.y += tile_size
                self.walk_cooldown = self.walk_cooldown_max
            elif keys[K_a]:
                self.rect.x -= tile_size
                self.walk_cooldown = self.walk_cooldown_max
            elif keys[K_d]:
                self.rect.x += tile_size
                self.walk_cooldown = self.walk_cooldown_max

def main():
    player = Player(1, 1)
    while True:
        screen.fill("#FFFFFF")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.update()
        player.draw(screen)

        true_screen.blit(pygame.transform.scale(screen, true_screen.get_rect().size), (0, 0))
        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()
