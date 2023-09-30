#### IMPORTS
import pygame, sys

from settings import *

class Main:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()

	def run(self):
		while True:
			dt = self.clock.tick() / 1000 # delta time
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			pygame.display.update()

if __name__ == '__main__':
	main = Main()
	main.run()