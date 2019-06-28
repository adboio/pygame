import pygame
import random
import time

WIDTH = 800
HEIGHT = 600
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

score = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump and Duck")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, BLACK)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50, 100))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.speedx = 10
		self.speedy = 60
		self.rect.x = 50
		self.rect.y = HEIGHT - self.rect.height - 20
		self.jumping = False
		self.jump_count = 0
		self.lives = 3

	def update(self):
		self.speedx = 0

		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.speedx = -20
		if keys[pygame.K_RIGHT]:
			self.speedx = 20

		self.rect.x += self.speedx

		if self.jumping:
			if self.jump_count < 10:
				self.rect.y -= self.speedy
				self.jump_count += 1

			elif self.jump_count >= 10 and self.jump_count < 20:
				self.rect.y += self.speedy
				self.jump_count += 1

			elif self.jump_count >= 20:
				self.jumping = False
				self.jump_count = 0

		if self.rect.left < 10:
			self.rect.left = 10
		if self.rect.right > WIDTH - 10:
			self.rect.right = WIDTH - 10



	def jump(self):
		if not self.jumping:
			self.jumping = True

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50, 50))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.speedx = -10
		self.rect.x = WIDTH + 20
		self.rect.y = HEIGHT - self.rect.height - random.randrange(20, 200)

	def update(self):
		global score

		self.rect.x += self.speedx

		if self.rect.right < 0:
			score += 1
			self.kill()


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True
while running:

	clock.tick(FPS)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.jump()

	if len(enemies.sprites()) < 3:
		enemy_spawn = random.randint(1, 10)
		if enemy_spawn == 2:
			e = Enemy()
			all_sprites.add(e)
			enemies.add(e)

	player.update()
	enemies.update()

	hits = pygame.sprite.spritecollide(player, enemies, True)
	if hits:
		player.lives -= 1
		if player.lives <= 0:
			running = False


	screen.fill(GREEN)
	all_sprites.draw(screen)

	draw_text(screen, 'Score: ' + str(score), 18, WIDTH - 100, 20)
	draw_text(screen, 'Lives: ' + str(player.lives), 18, WIDTH - 100, 40)

	pygame.display.flip()

pygame.quit()
