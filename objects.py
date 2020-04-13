from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame import Surface
from pygame.image import load

class Ground(Sprite):
	image = load('images/objects/ground.png')
	state = 'ground'
	def __init__(self, x, y):
		Sprite.__init__(self)
		self.rect = Rect(x, y, 40, 40)

	def draw(self, surface):
		surface.blit(self.image, self.rect.topleft)

class Stone(Ground):
	image = load('images/objects/stone.png')

class Trap(Ground):
	image = load('images/objects/trap_box.png')
	state = 'trap'

class Enemy(Ground):
	image = load('images/objects/enemy.png')
	state = 'enemy'

class Target(Ground):
	image = load('images/objects/target.png')
	state = 'target'

class Upper(Ground):
	image = load('images/objects/upper.png')
	state = 'upper'


class Camera(object):
	def __init__(self, target, resolution, screen_resolution):
		self.target = target
		self.width, self.height = resolution
		self.screen_width, self.screen_height = screen_resolution

	def get_pos(self):
		x = 0
		y = 0
		if self.target.rect.x > self.screen_width // 2:
			x = -(self.target.rect.x - self.screen_width // 2)
		if self.target.rect.x - self.screen_width//2 > self.width - self.screen_width:
			x = -(self.width - self.screen_width)
		if self.target.rect.y > self.screen_height // 2:
			y = -(self.target.rect.y - self.screen_height // 2)
		if self.target.rect.y - self.screen_height//2 > self.height - self.screen_height:
			y = -(self.height - self.screen_height)
		return (x, y)
