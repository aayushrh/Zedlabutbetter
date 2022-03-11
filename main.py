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
	def __init__(self, w, h, xo, yo, cool, s, pl):
		self.dur = cool
		self.cooldown = 0
		self.pl = pl
		self.xo, self.yo = xo, yo
		self.image = pygame.Surface((w, h))
		self.rect = pygame.Rect((0, 0), self.image.get_size())
		self.rect.x = self.pl.rect.centerx + (xo * s)
		self.rect.centery = pl.rect.centery + yo
		self.s = s
		pl.occ = True
		
	def update(self):
		self.cooldown += 1
		if self.cooldown >= self.dur:
			self.end()
			return False
		self.rect.centerx=self.pl.rect.centerx+(self.xo*self.s)
		self.rect.centery = self.pl.rect.centery + self.yo
		
		for p in self.pl.plg.sprites():
			if self.pl != p:
				if self.rect.colliderect(p.rect):
					p.acelx += 5 * self.s
					
					p.onground = False
					p.rect.y -= 1
					p.acely -= 5
					
					p.hp -= 1
					print(p.hp)
		
		return True
			
	def draw(self):
		SCREEN.blit(self.image, self.rect)

	def end(self):
		self.pl.occ = False
		self.pl.att = None

class Player(pygame.sprite.Sprite):
	def __init__(self, plg, width, height, x, y, speed, hp, jpheight, keys):
		super().__init__()
		self.image = pygame.Surface((width, height))
		self.rect = pygame.Rect((x, y), self.image.get_size())
		self.keys = keys
		self.speed = speed
		self.acely = 0
		self.acelx = 0.0
		self.onground = True
		self.jpheight = jpheight
		self.occ = False
		self.att = None
		self.plg = plg
		self.hp = hp
		
	def update(self):
		self.acelx -= (0.5 if self.acelx > 0 else (-0.5 if self.acelx < 0 else 0))
		self.acelx = clamp(-5, self.acelx, 5)
		pkeys = pygame.key.get_pressed()
		
		if not self.occ:
			if pkeys[self.keys["sp"]]:
				if pkeys[self.keys["rt"]]:
					self.att=Attack(30, 10, 10, -5, 10, 1, self)
				if pkeys[self.keys["lf"]]:
					self.att=Attack(30,10, 10, -5, 10, -1, self)
			else:
				if pkeys[self.keys["rt"]]:
					self.acelx += 1
				if pkeys[self.keys["lf"]]:
					self.acelx -= 1
					
		# things to happen regardless of special press
		
		self.onground = self.rect.bottom >= GROUNDLVL
		if not self.onground:
			self.acely += 1
		else:
			self.acely = 0
			self.rect.bottom = GROUNDLVL
			if pkeys[self.keys["jp"]] and not self.occ:
				self.acely = -self.jpheight
			
		self.rect.x += (self.acelx * self.speed)
		self.rect.x = clamp(0, self.rect.x, W-self.rect.width)
		self.rect.y += self.acely
		
		
		if self.att:
			if self.att.update():
				self.att.draw()
		

def main():
	plgroup = pygame.sprite.Group()
	plgroup.add(Player(plgroup, 20, 50, 10, 10, 4, 15, 10, {
		"lf": pygame.K_a,
		"rt": pygame.K_d,
		"jp": pygame.K_w,
		"sp": pygame.K_s
	}))
	plgroup.add(Player(plgroup, 20, 50, W-30, 10, 2, 20, 10, {
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
