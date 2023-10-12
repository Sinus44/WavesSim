import pygame
import time
import threading
from multiprocessing import Process
import sys

sys.setrecursionlimit(20000)

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

class Cargo:
	def __init__(self, y, speedy, mass, static = False, i = -1, j = -1):
		self.y = y
		self.speedy = speedy
		self.static = static
		self.mass = mass or 1
		self.links = []
		self.neary = 0
		self.linked = 0
		self.i = i
		self.j = j

	def add_link(self, cargo):
		self.links.append(cargo)
		self.linked += 1
		cargo.links.append(self)
		cargo.linked += 1

class Simulation:
	def __init__(self):
		self.enable = False
		self.screen_mode = False
		self.view_mode = False
		self.w = 0
		self.h = 0
		self.frame = 0

		self.speed = 1
		self.frame_rate = 100
		
		self.frame_time = 1 / self.frame_rate
		self.size = 15

		self.change_screen_mode()
		self.sizew = self.w // self.size
		self.sizeh = self.h // self.size
		self.generate_cargos()
		self.colors = [[[0, 0] for j in range(self.sizew)] for i in range(self.sizeh)]

	def intersection(self, i, j=0):
		return 0 <= i < self.sizeh and 0 <= j < self.sizew 

	def generate_cargos(self):
		self.cargos = [[Cargo(
			0, # Start Y
			0, # Start speed
			100 if (((self.sizeh//2)-i+20) **2 + ((self.sizew // 2)-j)**2)**0.5 < 15 else 1 , # Mass
			False,
			#j == 6 and i != self.sizeh//2-3 and i!= self.sizeh//2+3,
			i, j
			) for j in range(self.sizew)] for i in range(self.sizeh)]


		for i, line in enumerate(self.cargos):
			for j, cargo in enumerate(line):

				if self.intersection(i - 1, j):
					cargo.add_link(self.cargos[i - 1][j])

				if self.intersection(i + 1, j):
					cargo.add_link(self.cargos[i + 1][j])
				
				if self.intersection(i, j - 1):
					cargo.add_link(self.cargos[i][j - 1])
				
				if self.intersection(i, j + 1):
					cargo.add_link(self.cargos[i][j + 1])

		self.cargos[20][20].speedy = 10000
		

	def change_screen_mode(self):
		if not self.screen_mode:
			self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		else:
			self.screen = pygame.display.set_mode((1440, 900))

		self.screen_mode = not self.screen_mode
		self.w = screen.get_width()
		self.h = screen.get_height()
		pygame.display.set_caption('SpringPy')

	def start(self):
		self.enable = True
		while self.enable:
			stime = time.time()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit()

				if event.type == pygame.KEYDOWN:
					if event.unicode.lower() == "f":
						self.change_screen_mode()

			for line in self.cargos:
				for cargo in line:
					
					cargo.speedy += ((cargo.neary / cargo.linked) - cargo.y) / cargo.mass
					cargo.neary = 0

			print(f"S-time: {time.time() - stime}")
			dtime = time.time()



			for line in self.cargos:
				for cargo in line:
					#if cargo.static:
					#	continue
					if not cargo.static:
						cargo.y += cargo.speedy * self.speed

						for link in cargo.links:
							link.neary += cargo.y

						color = max(min(int(cargo.y / self.h * 255), 255), 0)
					
					else:
						color = 255

					self.colors[cargo.i][cargo.j][0] += color
					self.colors[cargo.i][cargo.j][1] += 1
					
					if not self.view_mode:
						pygame.draw.rect(self.screen, (color, color, color), (self.size * cargo.j, self.size * cargo.i, self.size, self.size))


					#print(color)

			if self.view_mode:
				for i, line in enumerate(self.colors):
					for j, pixel in enumerate(line):
						color = pixel[0] / pixel[1]
						pygame.draw.rect(self.screen, (color, color, color), (self.size * j, self.size * i, self.size, self.size))

			#print(f"D-time: {time.time() - dtime}")
			pygame.display.flip()
			#time.sleep(self.frame_time)

if __name__ == "__main__":
	sim = Simulation()
	sim.start()