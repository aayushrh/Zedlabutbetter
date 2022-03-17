import pygame, sys, math, copy
from math import radians, degrees
pygame.init()
pygame.font.init()
fps = 30
clock = pygame.time.Clock()
width, height = 256, 256
true_screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
screen = pygame.Surface((width, height))

def inverse(m):
		out = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		out[0][1] = m[1][0]
		out[0][2] = m[2][0]
		out[1][0] = m[0][1]
		out[1][2] = m[2][1]
		out[1][0] = m[0][1]
		out[2][0] = m[0][2]
		out[3][0] = -(m[3][0] * m[0][0] + m[3][1] * m[1][0] + m[3][2] * m[2][0])
		out[3][1] = -(m[3][0] * m[0][1] + m[3][1] * m[1][1] + m[3][2] * m[2][1])
		out[3][2] = -(m[3][0] * m[0][2] + m[3][1] * m[1][2] + m[3][2] * m[2][2])
		out[3][3] = 1
		return out

def rotmatY(AngleRad):
	matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	matrix[0][0] = math.cos(AngleRad)
	matrix[0][2] = math.sin(AngleRad)
	matrix[2][0] = -math.sin(AngleRad)
	matrix[1][1] = 1
	matrix[2][2] = math.cos(AngleRad)
	matrix[3][3] = 1
	
class Vec3d:
	def __init__(self, x=None, y=None, z=None):
		self.x = x
		self.y = y
		self.z = z
	def normalize(self):
		l = math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
		try:
			self.x /= l
			self.y /= l
			self.z /= l
		except ZeroDivisionError:
			self.x = self.y = self.z = 0
	def matrixmultiply(self, m):
		out = Vec3d()
		out.x = self.x * m[0][0] + self.y * m[1][0] + self.z * m[2][0] + m[3][0]
		out.y = self.x * m[0][1] + self.y * m[1][1] + self.z * m[2][1] + m[3][1]
		out.z = self.x * m[0][2] + self.y * m[1][2] + self.z * m[2][2] + m[3][2]
		w = self.x * m[0][3] + self.y * m[1][3] + self.z * m[2][3] + m[3][3]
		
		if w != 0:
			out.x /= w
			out.y /= w
			out.z /= w
		return out
		
class Tri:
	def __init__(self, p1=None, p2=None, p3=None, col="#FFFFFF"):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.col = col
	def draw(self):
		pygame.draw.polygon(screen, self.col, ((self.p1.x, self.p1.y), (self.p2.x, self.p2.y), (self.p3.x, self.p3.y)))
	def draw_wireframe(self):
		pygame.draw.lines(screen, "#AAAA00", True,  ((self.p1.x, self.p1.y), (self.p2.x, self.p2.y), (self.p3.x, self.p3.y)))
	def matrixmultiply(self, m):
		out = Tri(col = self.col)
		out.p1 = self.p1.matrixmultiply(m)
		out.p2 = self.p2.matrixmultiply(m)
		out.p3 = self.p3.matrixmultiply(m)
		return out
			
class Mesh:
	def __init__(self, tris=[]):
		self.tris = tris
	def loadfromfile(self, path):
		verts = []
		with open(path) as f:
			data = f.read().split('\n')
			for l in data:
				try:
					if l[0] == 'v':
						vals = l[2:].split()
						verts.append(Vec3d(float(vals[0]), float(vals[1]), float(vals[2])))
					elif l[0] == 'f':
						vals = l[2:].split()
						self.tris.append(Tri(verts[int(vals[0])-1],verts[int(vals[1])-1],verts[int(vals[2])-1]))
				except IndexError:
					pass

class Engine:
	def __init__(self):
		self.cube = Mesh()
		self.cube.loadfromfile("ship.obj")
		
		self.vcam = Vec3d(0, 0, 0)
		self.vlook = Vec3d(0, 0, 1)
		self.rendermode = "normal"
		
		self.nearclip = 0.1
		self.farclip = 1000
		self.fov = 90
		self.aspectratio = height/width
		self.fovrad = (1/math.tan(radians(self.fov * 0.5)))

		self.matproj = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		self.matproj[0][0] = self.fovrad * self.aspectratio
		self.matproj[1][1] = self.fovrad
		self.matproj[2][2] = self.farclip / (self.farclip - self.nearclip)
		self.matproj[3][2] = (-self.farclip * self.nearclip) / (self.farclip - self.nearclip)
		self.matproj[2][3] = 1

		self.theta = 0
		self.matrotx = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		self.matrotz = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		self.camroty = 0

	def update(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_q]:
			self.vcam.y += 8 * (1/fps)
		if keys[pygame.K_e]:
			self.vcam.y -= 8 * (1/fps)
		if keys[pygame.K_w]:
			self.vcam.z -= 8 * (1/fps)
		if keys[pygame.K_s]:
			self.vcam.z += 8 * (1/fps)
		if keys[pygame.K_a]:
			self.camroty += 8 * (1/fps)
		if keys[pygame.K_d]:
			self.camroty -= 8 * (1/fps)
		
		#self.theta += 1 * 1/fps
		
		self.vup = Vec3d(0, 1, 0)
		self.vtar = Vec3d(self.vcam.x+self.vlook.x, self.vcam.y+self.vlook.y, self.vcam.z+self.vlook.z)
		self.camrotmat = rotmatY(self.camroty)
		self.vlook = self.vtar.matrixmultiply(self.camrotmat)
		self.vtar = Vec3d(self.vcam.x + self.vlook.x, self.vcam.y + self.vlook.y, self.vcam.z + self.vlook.z)
		self.vcam = Vec3d(0, 0, 0)
		
		newF = Vec3d(self.vtar.x - self.vcam.x, self.vtar.y - self.vcam.y, self.vtar.z - self.vcam.z)
		newF.normalize()
		
		dp = self.vup.x*newF.x+self.vup.y*newF.y+self.vup.z*newF.z
		a = Vec3d(newF.x*dp, newF.y*dp, newF.z*dp)
		newU = Vec3d(self.vup.x-a.x, self.vup.y-a.y, self.vup.z-a.z)
		newU.normalize()
		
		newR = Vec3d()
		
		newR.x = newU.y * newF.z - newU.z * newF.y
		newR.y = newU.z * newF.x - newU.x * newF.z
		newR.z = newU.x * newF.y - newU.y * newF.x
		
		self.matcam =  [[newR.x,newR.y,newR.z,0],
				  [newU.x,newU.y,newU.z,0],
				  [newF.x,newF.y,newF.z,0],
				  [self.vcam.x,self.vcam.y,self.vcam.z,1]]
		
		
		self.matview = inverse(self.matcam)
		
		self.matrotz[0][0] = math.cos(self.theta)
		self.matrotz[0][1] = math.sin(self.theta)
		self.matrotz[1][0] = -math.sin(self.theta)
		self.matrotz[1][1] = math.cos(self.theta)
		self.matrotz[2][2] = 1
		self.matrotz[3][3] = 1
			
		self.matrotx[0][0] = 1
		self.matrotx[1][1] = math.cos(self.theta*0.5)
		self.matrotx[1][2] = math.sin(self.theta*0.5)
		self.matrotx[2][1] = -math.sin(self.theta*0.5)
		self.matrotx[2][2] = math.cos(self.theta*0.5)
		self.matrotx[3][3] = 1
		
		tristodraw = []
		
		for tri in self.cube.tris:
			translated = copy.deepcopy(tri)
			
			translated = translated.matrixmultiply(self.matrotz)
			translated = translated.matrixmultiply(self.matrotx)
			
			translated.p1.z += 8
			translated.p2.z += 8
			translated.p3.z += 8
			
			tristodraw.append(translated)
		
		tristodraw.sort(key=lambda x: (x.p1.z+x.p2.z+x.p3.z)/3, reverse=True)
		
		for tri in tristodraw:
			line1 = Vec3d(tri.p2.x - tri.p1.x, tri.p2.y - tri.p1.y, tri.p2.z - tri.p1.z)
			line2 = Vec3d(tri.p3.x - tri.p1.x, tri.p3.y - tri.p1.y, tri.p3.z - tri.p1.z)
			normal = Vec3d()
			normal.x = line1.y * line2.z - line1.z * line2.y
			normal.y = line1.z * line2.x - line1.x * line2.z
			normal.z = line1.x * line2.y - line1.y * line2.x
			normal.normalize()
			camray = Vec3d(tri.p1.x - self.vcam.x, tri.p1.y - self.vcam.y, tri.p1.z - self.vcam.z)
			if ((normal.x*camray.x + normal.y*camray.y + normal.z*camray.z) < 0) or "all" in self.rendermode:
				
				viewed = copy.deepcopy(tri)
				viewed.p1 = tri.p1.matrixmultiply(self.matcam)
				viewed.p2 = tri.p2.matrixmultiply(self.matcam)
				viewed.p3 = tri.p3.matrixmultiply(self.matcam)
				
				lightdir = Vec3d(0, 0, -1)
				lightdir.normalize()
				dp = max(0.1, lightdir.x*normal.x + lightdir.y*normal.y + lightdir.z*normal.z)
				projected = viewed.matrixmultiply(self.matproj)
				projected.col = (dp*255,dp*255,dp*255)

				projected.p1.x += 1
				projected.p1.y += 1
				projected.p2.x += 1
				projected.p2.y += 1
				projected.p3.x += 1
				projected.p3.y += 1

				projected.p1.x *= 0.5 * width
				projected.p1.y *= 0.5 * height
				projected.p2.x *= 0.5 * width
				projected.p2.y *= 0.5 * height
				projected.p3.x *= 0.5 * width
				projected.p3.y *= 0.5 * height

				if "normal" in self.rendermode:
					projected.draw()
				if "wireframe" in self.rendermode:
					projected.draw_wireframe()


def main():
	engine = Engine()
	oldticks = pygame.time.get_ticks()
	while True:
		screen.fill("#000000")
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		screen.blit(pygame.font.Font(None,20).render(str(round(1/((pygame.time.get_ticks()-oldticks)/1000))),False,"#FFFFFF"), (0, 0))
		oldticks = pygame.time.get_ticks()
		
		engine.update()

		true_screen.blit(pygame.transform.scale(screen, true_screen.get_size()), (0, 0))
		pygame.display.flip()
		clock.tick(fps)


if __name__ == "__main__":
	main()
