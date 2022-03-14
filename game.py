import json
from os import listdir
from time import time
import pygame
from player import Player
from objects import (Ground, Camera, Stone,
	Trap, Enemy, Target, Upper)


FPS = 60
BLOCK_SIZE = 40

class Game:
	def __init__(self, level_path, music_path,
			resolution, fullscreen):
		pygame.init()
		pygame.mixer.music.load(music_path)
		pygame.mixer.music.play(-1)
		self.window = pygame.display.set_mode(resolution,
			pygame.FULLSCREEN if fullscreen else 0)
		self.resolution = self.window.get_width(), self.window.get_height()
		pygame.display.set_caption('410')
		self.root = None
		self.timer = pygame.time.Clock()
		self.font = pygame.font.SysFont("calibri", 30, 1)
		with open(level_path) as file:
			lines = [line.strip() for line in file.readlines()]
			self.objects = self.create_level(lines)
		self.start_time = time()

	def create_level(self, level):
		height = len(level)
		width = max(len(string) for string in level)
		self.level_width, self.level_height = width*BLOCK_SIZE, height*BLOCK_SIZE
		self.root = pygame.Surface((width * BLOCK_SIZE, height * BLOCK_SIZE))
		all(width == len(row) for row in level)
		objects = pygame.sprite.Group()
		x = y = 0
		for row in level:
			for col in row:
				if col == '-':
					objects.add(Ground(x, y))
				elif col == '#':
					objects.add(Stone(x, y))
				elif col == 't':
					objects.add(Trap(x, y))
				elif col == 'p':
					self.player = Player(x, y)
				elif col == 'e':
					objects.add(Enemy(x, y))
				elif col == 'T':
					objects.add(Target(x, y))
				elif col == 'u':
					objects.add(Upper(x, y))
				x += BLOCK_SIZE
			y += BLOCK_SIZE
			x = 0
		self.camera = Camera(self.player,
				(width * BLOCK_SIZE, height * BLOCK_SIZE), self.resolution)
		return objects

	def draw(self):
		self.window.fill((0, 0, 0))
		self.root.fill((0, 0, 0))

		if self.player.win:
			text = self.font.render('LEVEL COMPLITED!  Time: {}s'.format(str(self.end_time)),
				1, (0, 255, 255))
			self.window.blit(text, (self.resolution[0]//4, self.resolution[1]//4))
			pygame.display.update()
			self.timer.tick(FPS)
			return
		elif self.player.lose_reload:
			self.player.lose_reload -= 1
			text = self.font.render('GAME OVER',
				1, (0, 255, 255))
			self.window.blit(text, (self.resolution[0]//4, self.resolution[1]//4))
			pygame.display.update()
			self.timer.tick(FPS)
			return

		self.objects.draw(self.root)
		self.player.draw(self.root)
		

		self.window.blit(self.root, self.camera.get_pos())

		self.end_time = round(time()-self.start_time, 2)
		text = self.font.render('Time: {}s'.format(str(self.end_time)),
			1, (255, 255, 255))
		self.window.blit(text, (10, 10))

		pygame.display.update()
		self.timer.tick(FPS)

	def run(self):
		while True:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return

			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				pygame.quit()
				return
			mouse_pos = pygame.mouse.get_pos()
			left = keys[pygame.K_a]
			right = keys[pygame.K_d]
			up = keys[pygame.K_SPACE]
			if pygame.mouse.get_pressed()[0]:
				left = mouse_pos[0] < self.resolution[0]//2
				right = mouse_pos[0] > self.resolution[0]//2
				up = keys[pygame.K_w] or mouse_pos[1] < self.resolution[1]//2
			self.player.update(left, right, up,	self.objects)

			if self.player.rect.top > self.level_height*3:
				self.player.rect.x, self.player.rect.y = self.player.start_pos
			self.draw()



def main(args):
	Game(level_path=args['level'], music_path=args['music'],
		resolution=args['resolution'], fullscreen=args['fullscreen']).run()


if __name__ == '__main__':
	main({
		'level': 'levels/2.lvl',
		'music': 'music/Bloody Stream.mp3',
		'resolution': [0, 0],
		'fullscreen': True,
		})