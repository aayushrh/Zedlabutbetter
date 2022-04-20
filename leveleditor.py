import sys, pygame
from math import floor

pygame.init()

WIDTH, HEIGHT = 1024, 576
TDIMS = 32

FPS = 60
CLOCK = pygame.time.Clock()
TRUE_SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
SCREEN = pygame.Surface((WIDTH, HEIGHT))

BLACK = "#000000"
WHITE = "#FFFFFF"


class Tile(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.Surface((TDIMS, TDIMS))
		self.image.fill(WHITE)
		self.rect = pygame.Rect((x, y), self.image.get_size())


def main():
	tilegroup = pygame.sprite.Group()

	while True:
		SCREEN.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				matrix = []
				for y in range(0, HEIGHT, 32):
					toadd = []
					for x in range(0, WIDTH, 32):
						added = False
						print(x)
						for t in tilegroup.sprites():
							if t.rect.x == x and t.rect.y == y:
								toadd.append(1)
								added = True
								break
						if not added:
							toadd.append(0)
					matrix.append(toadd)
				
				with open("level.py", 'a') as f:
					try:
						f.write(f"\n{sys.argv[1]} = {matrix}")
					except:
						f.write(f"\ntime{pygame.time.get_ticks()} = {matrix}")
				
				pygame.quit()
				sys.exit()

		if pygame.mouse.get_pressed()[0]:
			x, y = pygame.mouse.get_pos()
			x = floor(x/32)*32
			y = floor(y/32)*32
			shouldadd = True
			for t in tilegroup.sprites():
				if t.rect.x == x and t.rect.y == y:
					shouldadd = False
					break
			if shouldadd:
				tilegroup.add(Tile(x, y))
		if pygame.mouse.get_pressed()[2]:
			x, y = pygame.mouse.get_pos()
			x = floor(x/32)*32
			y = floor(y/32)*32
			for t in tilegroup.sprites():
				if t.rect.x == x and t.rect.y == y:
					tilegroup.remove(t)
					break
				
		tilegroup.update()

		tilegroup.draw(SCREEN)

		TRUE_SCREEN.blit(pygame.transform.scale(SCREEN, TRUE_SCREEN.get_size()), (0, 0))
		pygame.display.flip()
		CLOCK.tick(FPS)


if __name__ == "__main__":
	main()
