import sys
import pygame
from pygame import K_w, K_a, K_s, K_d, K_SPACE
from random import randint
pygame.init()

fps = 8
clock = pygame.time.Clock()
width, height = 16*16, 9*16
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
		self.target = True # true for player, false for anti
		self.targetcool = 1
		self.sight = 10
		self.knockback = 3
		
	def update(self, pl):
		self.targetcool -= 1
		if self.targetcool <= 0:
			self.target = bool(randint(0, 1))
			self.targetcool = 32
		player = (pl if self.target else Player(width/tile_size-pl.x,pl.y))
		xmove = self.x + ((-abs(self.x - player.x)/(self.x - player.x)) if (self.x - player.x) != 0 else 0)
		ymove = self.y + ((-abs(self.y - player.y)/(self.y - player.y)) if (self.y - player.y) != 0 else 0)
		distx = ((player.x-xmove)**2 + (player.y-self.y)**2)**0.5 + randint(-self.sight, self.sight)
		disty = ((player.x-self.x)**2 + (player.y-ymove)**2)**0.5 + randint(-self.sight, self.sight)
		if distx < disty:
			self.x = xmove
		else:
			self.y = ymove
		if player.sword:
			if player.sword.x == self.x and pl.sword.y == self.y:
				self.x += player.sword.d[0]*self.knockback
				self.y += player.sword.d[1]*self.knockback
		
		
		self.rect.x = self.x*tile_size
		self.rect.y = self.y*tile_size
		
class Weapon:
	def __init__(self, x, y, d):
		self.x = x
		self.y = y
		self.d = d
		self.image = pygame.Surface((tile_size, tile_size))
		self.rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
		
	def draw(self):
		screen.blit(self.image, (self.rect.x, self.rect.y))

class Player:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.image = pygame.Surface((tile_size, tile_size))
		self.rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
		self.dir = [0, 0]
		self.sword = None
		self.insafeplace = False
		self.swordcool = 0

	def draw(self):
		screen.blit(self.image, (self.rect.x, self.rect.y))

	def update(self):
		self.sword = None
		self.swordcool -= 1
		keys = pygame.key.get_pressed()
		if keys[K_SPACE] and not self.insafeplace and self.swordcool <= 0:
			self.sword = Weapon(self.x + self.dir[0], self.y + self.dir[1], self.dir)
			self.sword.draw()
			self.swordcool = 2
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
				
				
		self.rect.y = self.y*tile_size
		self.rect.x = self.x*tile_size

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

		player.update()
		player.draw()


		enim_group.update(player)
		enim_group.draw(screen)	


		true_screen.blit(pygame.transform.scale(screen, true_screen.get_rect().size), (0, 0))
		pygame.display.flip()
		clock.tick(fps)

if __name__ == "__main__":
	main()
