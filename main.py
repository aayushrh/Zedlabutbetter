import pygame, sys
from random import randint
pygame.init()
FPS = 60
CLOCK = pygame.time.Clock()
W, H = 720, 360
TRUE_SCREEN = pygame.display.set_mode((W, H), pygame.RESIZABLE)
SCREEN = pygame.Surface((W, H))
GROUNDLVL = H

def clamp(smallest, n, largest): 
	return max(smallest, min(n, largest))

class Attack:
	def __init__(self, xo, yo, pl):
		self.dur = 50
		self.cooldown = 0
		self.pl = pl
		self.xo, self.yo = xo, yo
		self.image = pygame.Surface((10, 10))
		self.rect = pygame.Rect((pl.rect.x + xo, pl.rect.y + yo), self.image.get_size())
		
	def update(self):
		self.cooldown += 1
		if self.cooldown >= self.dur:
			self.end()
			return False
		self.rect.x = self.pl.rect.x + self.xo * self.pl.dir
		self.rect.y = self.pl.rect.y + self.yo * self.pl.dir
		return True
			
	def draw(self):
		SCREEN.blit(self.image, self.rect)

	def end(self):
		self.pl.occ = False
		self.pl.att = None

class Player(pygame.sprite.Sprite):
	def __init__(self, width, height, x, y, speed, jpheight, keys):
		super().__init__()
		self.image = pygame.Surface((width, height))
		self.rect = pygame.Rect((x, y), self.image.get_size())
		self.keys = keys
		self.speed = speed
		self.acely = 0
		self.acelx = 0
		self.onground = True
		self.jpheight = jpheight
		self.occ = False
		self.att = None
		self.dir = 0
		
	def netrualside(self, s):
		self.occ = True
		self.att = Attack(-self.rect.width if s == 'l' else self.rect.width, 0, self)
		
	def update(self):
		self.acelx *= 0.6
		print(round(self.acelx*100))
		pkeys = pygame.key.get_pressed()
		self.dir = 0
		if not self.occ:
			if pkeys[self.keys["sp"]]:
				if pkeys[self.keys["lf"]]:
					self.netrualside('l')
					self.dir = -1
				if pkeys[self.keys["rt"]]:
					self.netrualside('r')
					self.dir = 1
			else:
				if pkeys[self.keys["lf"]]:
					self.dir = -1
					self.acelx -= 1
				if pkeys[self.keys["rt"]]:
					self.dir = 1
					self.acelx += 1
			
		
			self.onground = self.rect.bottom >= GROUNDLVL
			if not self.onground:
				self.acely += 1
			else:
				self.acely = 0
				self.rect.bottom = GROUNDLVL
				if pkeys[self.keys["jp"]]:
					self.acely = -self.jpheight
		
		# things to happen regardless of special press
		
		if self.att:
			if self.att.update():
				self.att.draw()
		
		#self.acelx = round(clamp(-2, self.acelx, 2)*10)/10
		self.rect.x += (self.acelx * self.speed)
		self.rect.x = clamp(0, self.rect.x, W-self.rect.width)
		self.rect.y += self.acely
		

def main():
	plgroup = pygame.sprite.Group()
	plgroup.add(Player(20, 50, 10, 10, 4, 15, {
		"lf": pygame.K_a,
		"rt": pygame.K_d,
		"jp": pygame.K_w,
		"sp": pygame.K_s
	}))
	plgroup.add(Player(20, 50, W-30, 10, 2, 20, {
		"lf": pygame.K_LEFT,
		"rt": pygame.K_RIGHT,
		"jp": pygame.K_UP,
		"sp": pygame.K_DOWN
	}))
	while True:
		SCREEN.fill("#FFFFFF")
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		
		plgroup.update()
		
		plgroup.draw(SCREEN)

		TRUE_SCREEN.blit(pygame.transform.scale(SCREEN, TRUE_SCREEN.get_size()), (0, 0))
		pygame.display.flip()
		CLOCK.tick(FPS)

if __name__ == "__main__":
	main()
