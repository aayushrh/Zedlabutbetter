import sys
import pygame
from pygame import K_w, K_a, K_s, K_d, K_SPACE
from random import randint
pygame.init()

fps = 8
clock = pygame.time.Clock()
width, height = 256, 160
true_screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
screen = pygame.Surface((width, height))
tile_size = 16

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.x = x
		self.y = y
		self.image = pygame.Surface((tile_size, tile_size))
		self.wepimg = pygame.Surface((tile_size, tile_size))
		self.rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
		
	def update(self):
		self.x += randint(-1,1)
		
		
		
		self.rect.x = self.x*16
		self.rect.y = self.y*16

class Player:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.image = pygame.Surface((tile_size, tile_size))
		self.wepimg = pygame.Surface((tile_size, tile_size))
		self.rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
		self.dir = [0, 0]
		self.insafeplace = False

	def draw(self):
		screen.blit(self.image, (self.rect.x, self.rect.y))

	def update(self):
		keys = pygame.key.get_pressed()
		if keys[K_SPACE] and not self.insafeplace:
			screen.blit(self.wepimg, ((self.x+self.dir[0])*16, (self.y+self.dir[1])*16))
		elif keys[K_w]:
			self.dir = [0, -1]
			self.y -= 1
		elif keys[K_s]:
			self.dir = [0, 1]
			self.y += 1
		elif keys[K_a]:
			self.dir = [-1, 0]
			self.x -= 1
		elif keys[K_d]:
			self.dir = [1, 0]
			self.x += 1
				
				
		self.rect.y = self.y*16
		self.rect.x = self.x*16

def main():
	player = Player(15//2, 9//2)
	
	enim_group = pygame.sprite.Group()
	enim_group.add(Enemy(1, 1))
	while True:
		screen.fill("#FFFFFF")

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		enim_group.update()
		enim_group.draw(screen)	
				
		player.update()
		player.draw()
		

		true_screen.blit(pygame.transform.scale(screen, true_screen.get_rect().size), (0, 0))
		pygame.display.flip()
		clock.tick(fps)

if __name__ == "__main__":
	main()
