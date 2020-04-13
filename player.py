from pygame.sprite import Sprite
from pygame import Surface
from pygame.rect import Rect
from pygame.mixer import Sound
from pyganim import PygAnimation


MOVE_SPEED = 7
JUMP_POWER = 10
GRAVITY = 0.5
MAX_GRAVITY = 20
COLOR = (10, 10, 10)

ANIM_DELAY = 0.2
ANIM_STAY = (
	('images/player/stay1.png', ANIM_DELAY),
	('images/player/stay2.png', ANIM_DELAY),
)
ANIM_RIGHT = (
	('images/player/right1.png', ANIM_DELAY),
	('images/player/right2.png', ANIM_DELAY),
)
ANIM_LEFT = (
	('images/player/left1.png', ANIM_DELAY),
	('images/player/left2.png', ANIM_DELAY),
)
ANIM_JUMP = (
	('images/player/jump1.png', ANIM_DELAY * 2),
	('images/player/jump2.png', ANIM_DELAY * 10**10),
)


class Player(Sprite):
	def __init__(self, x, y):
		Sprite.__init__(self)
		self.xvel = 0
		self.yvel = 0
		self.on_ground = False
		self.start_pos = x, y
		self.image = Surface((40, 40))
		self.image.fill(COLOR)
		self.rect = Rect(x, y, 40, 40)
		self.image.set_colorkey(COLOR)
		self.jump_sound = Sound('sounds/jump.ogg')
		self.punch_sound = Sound('sounds/punch.ogg')
		self.anim_stay = PygAnimation(ANIM_STAY)
		self.anim_right = PygAnimation(ANIM_RIGHT)
		self.anim_left = PygAnimation(ANIM_LEFT)
		self.anim_jump = PygAnimation(ANIM_JUMP)
		self.anim_stay.play()
		self.anim_left.play()
		self.anim_right.play()
		self.anim_jump.play()
		self.anim_stay.blit(self.image, (0, 0))
		self.win = False
		self.lose_reload = 0

	def update(self, left, right, up, platforms):
		self.image.fill(COLOR)
		if right:
			self.xvel = MOVE_SPEED
			self.anim_right.blit(self.image, (0, 0))
		elif left:
			self.xvel = -MOVE_SPEED
			self.anim_left.blit(self.image, (0, 0))
		else:
			self.xvel = 0
			if not up:
				self.anim_stay.blit(self.image, (0, 0))
		
		if up:
			self.image.fill(COLOR)
			self.anim_jump.blit(self.image, (0, 0))
		else:
			self.anim_jump.rewind()

		if up and self.on_ground:
			self.yvel = -JUMP_POWER
			self.jump_sound.play()

		if not self.on_ground:
			self.yvel += GRAVITY if self.yvel + GRAVITY < MAX_GRAVITY else 0

		self.on_ground = False

		self.rect.y += self.yvel
		self.collide(0, self.yvel, platforms)

		self.rect.x += self.xvel # переносим свои положение на xvel
		self.collide(self.xvel, 0, platforms)

	def draw(self, surface):
		surface.blit(self.image, self.rect.topleft)

	def collide(self, xvel, yvel, platforms):
		for platform in platforms:
			if self.rect.colliderect(platform.rect):

				if platform.state == 'upper':
					self.yvel = -JUMP_POWER * 5
					continue

				if xvel > 0:
					self.rect.right = platform.rect.left

				if xvel < 0:
					self.rect.left = platform.rect.right

				if yvel > 0:
					self.rect.bottom = platform.rect.top
					self.on_ground = True
					self.yvel = 0

				if yvel < 0:
					self.rect.top = platform.rect.bottom
					self.yvel = 0

				if platform.state == 'trap':
					platforms.remove(platform)
					self.punch_sound.play()
				if platform.state == 'enemy':
					self.rect.x, self.rect.y = self.start_pos
					self.lose_reload = 60
				if platform.state == 'target':
					self.win = True


if __name__ == '__main__':
	Player(0, 0)