import sys, pygame
from math import floor
import level

pygame.init()

WIDTH, HEIGHT = 1024, 576
TDIMS = 32

FPS = 60
CLOCK = pygame.time.Clock()
TRUE_SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
SCREEN = pygame.Surface((WIDTH, HEIGHT))

BLACK = "#000000"
WHITE = "#FFFFFF"

def getmousepos():
	x, y = pygame.mouse.get_pos()
	w, h = TRUE_SCREEN.get_size()
	return (x/(w/WIDTH), y/(h/HEIGHT))

class Tile(pygame.sprite.Sprite):
	def __init__(self, x, y, mode):
		super().__init__()
		self.image = pygame.Surface((TDIMS, TDIMS))
		self.rect = pygame.Rect((x, y), self.image.get_size())
		self.type = mode
		# 0 is normal
		# 1 is kill
		# 2 is moving
		self.col = (WHITE if self.type == 0 else "#FF0000")
		self.image.fill(self.col)
		
def main():
	tilegroup = pygame.sprite.Group()
	mode = 1
	startpos = (0, 0)
	try:
		x, y = 0, 0
		for r in eval(f"level.{sys.argv[2]}"):
			for t in r:
				if t == 1:
					tilegroup.add(Tile(x, y, 0))
				if t == 3:
					tilegroup.add(Tile(x, y, 1))
				if t == 2:
					startpos = (x, y)
				x += 32
			y += 32
			x = 0
	except:
		pass
	
	while True:
		SCREEN.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				matrix = []
				for y in range(0, HEIGHT, 32):
					toadd = []
					for x in range(0, WIDTH, 32):
						added = False
						for t in tilegroup.sprites():
							if t.rect.x == x and t.rect.y == y:
								toadd.append(1 if t.type == 0 else (3 if t.type == 1 else 4))
								added = True
								break
						if not added:
							toadd.append(0 if ((x, y) != startpos) else 2)
					matrix.append(toadd)
				out = ""
				with open("level.py", 'r') as f:
					for l in f.read().split('\n'):
						if (not (sys.argv[1] in l)) and (not (l == '')):
							out += l + '\n'
				with open("level.py", 'w') as f:
					f.write(f"{out}\n{sys.argv[1]} = {matrix}")
				
				pygame.quit()
				sys.exit()
		
		keys = pygame.key.get_pressed()
		if keys[pygame.K_0]:
			mode = 0
		if keys[pygame.K_1]:
			mode = 1
		if keys[pygame.K_2]:
			mode = 2
		if keys[pygame.K_3]:
			mode = 3

		if pygame.mouse.get_pressed()[0]:
			x, y = getmousepos()
			x = floor(x/32)*32
			y = floor(y/32)*32
			if mode == 1 or mode == 3:
				shouldadd = True
				for t in tilegroup.sprites():
					if t.rect.x == x and t.rect.y == y:
						shouldadd = False
						break
				if shouldadd:
					tilegroup.add(Tile(x, y, (0 if mode==1 else 1)))
			if mode == 0:
				for t in tilegroup.sprites():
					if t.rect.x == x and t.rect.y == y:
						tilegroup.remove(t)
						break
			if mode == 2:
				startpos = (x, y)
						
		pos = getmousepos()
						
				
		tilegroup.update()
		
		toblit = pygame.Surface((TDIMS, TDIMS))
		toblit.fill("#aaaaaa" if mode == 1 else ("#88444444" if mode == 0 else ("#ddb500" if mode == 2 else "#ff0000")))
		SCREEN.blit(toblit, (floor(pos[0]/32)*32, floor(pos[1]/32)*32))
		tilegroup.draw(SCREEN)

		TRUE_SCREEN.blit(pygame.transform.scale(SCREEN, TRUE_SCREEN.get_size()), (0, 0))
		pygame.display.flip()
		CLOCK.tick(FPS)


if __name__ == "__main__":
	main()
