#### IMPORTS
import pygame
from pygame.image import load as loadImage

from settings import *
from editor import Editor

class Main:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()

		self.editor = Editor()

		## CURSOR
		cursor_surface = loadImage('graphics/cursors/mouse.png').convert_alpha()
		cursor = pygame.cursors.Cursor((0, 0), cursor_surface)
		pygame.mouse.set_cursor(cursor)

	def run(self):
		while True:
			dt = self.clock.tick() / 1000 # delta time
			
			self.editor.run(dt)
			pygame.display.update()


if __name__ == '__main__':
	main = Main()
	main.run()