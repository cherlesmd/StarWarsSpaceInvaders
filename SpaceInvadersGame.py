import os
import pygame
import time
import datetime
import random
from os import path

WIDTH = 460
HEIGHT = 600
FPS = 60

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
GREEN = (0, 255, 0)
BLUE = ( 0, 0, 255)
GRAY = (112, 118, 123)
YELLOW = (255, 255, 0)

#Directories for images
img_dir = path.join(path.dirname(__file__), 'imG')

#pygame.init() will initiate the game and load all elements needed for game setup
pygame.init()
#Creating a "Screen" variable to work with size HEIGHT and WIDTH.
#Width and height must be inside their own parenthesis as it is considered 1 object not 2 separate
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#Set caption
pygame.display.set_caption("Space Invaders")

#Game images
background  = pygame.image.load(path.join(img_dir, "hyperbackground.png")).convert()
background = pygame.transform.scale(background, (500, 600))
player_img = pygame.image.load(path.join(img_dir, "ship2.png")).convert_alpha()
player_bullet_img = pygame.image.load(path.join(img_dir, "laser.png")).convert_alpha()
enemy_bullet_img = pygame.image.load(path.join(img_dir, "bullet_enemy.png")).convert_alpha()
player_mini_img = pygame.transform.scale(player_img, (25, 25))
player_mini_img.set_colorkey(BLACK)
 

#--------- this block is for when the game level changes ---------
def level_change():
	#Boolean meant for keeping while loop running as the timer counts down
	alive = True
	#Remake sprites
	make_Enemies()
	player_bullets = pygame.sprite.Group()	
	enemy_bullets = pygame.sprite.Group()
	aliens = pygame.sprite.Group()
	#Mark current time and add 5 seconds
	start_time = int(time.time()) + 5
	#Recenter the player
	player.rect.centerx = WIDTH/2
	player.rect.bottom = HEIGHT - 30
	#While loop will continue until current time hits saved time from start_time + 5 seconds
	while alive: 	
		#passed_time is the variable keeping the while loop alive 
		passed_time = start_time - int(time.time())
		#Exit loop if the times equal each other
		if passed_time == 0:
			alive = False
		#If not 0, begin displaying screen with all black background
		screen.fill(BLACK)
		#Next we will draw the text letting the player know they have completed the level and the countdown from 5
		draw_text(screen, "LEVEL COMPLETED!", 40, WIDTH/2, HEIGHT/2, YELLOW)
		#Since we are running a while loop and passed_time is continously changing, it will continously change as the loop remains alive
		draw_text(screen, "Next level in " + str(passed_time) + " seconds", 40, WIDTH/2, HEIGHT/3, YELLOW)
		pygame.display.update()	
		pygame.display.flip()
	screen.fill(BLACK)
	pygame.display.update()	
	pygame.display.flip()
	game_loop()
#-----------------------------------------------------------------

def draw_lives(surf, x, y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		#MAKE SURE the algorithm is "x + 25 * i" not "x + 25 * 1"
		img_rect.x = x + 25 * i
		img_rect.y = y + 10
		surf.blit(img, img_rect)

def score(s):
	if s < 0:
		score.x = 0
	else:
		score.x += s
		return score.x
score.x = 0


def level(L):
	if L < 0:
		level.x = 0
	else:
		level.x += 1
		return level.x
level.x = 0

x_start = 40
x_end = 450
enemy_spawn_positions = []

while x_start <= x_end:
	enemy_spawn_positions.append(x_start)
	x_start += 40
	
row_of_enemies = 8
enemies = []

def make_Enemies():
	y = 50 
	for i in range(row_of_enemies):
		for index in enemy_spawn_positions:
			if i <= 2:
				enemy = Aliens(index, y, 1)
			elif i > 2 and i < 5:
				enemy = Aliens(index, y, 2)
			else:
				enemy = Aliens(index, y, 3)
			enemies.append(enemy)	
		y = y + 30
	for i in enemies:
		all_sprites.add(i)
		aliens.add(i)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(player_img, (25,25))
		self.rect = self.image.get_rect()
		self.radius = 12
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT - 30
		self.speedx = 0
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
		self.radius = int(self.rect.width/2)
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()


		
	def update(self):
	
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1800:
			self.hidden = False
			self.rect.centerx = WIDTH/2
			self.rect.bottom = HEIGHT - 30
			
		self.speedx = 0
		if self.hidden == True:
			keystate = pygame.K_DOWN
			for self in enemy_bullets:
				self.kill()
			for self in player_bullets:
				self.kill()
		
		else:
			keystate = pygame.key.get_pressed()
			if keystate[pygame.K_LEFT]:
				self.speedx = -5
			if keystate[pygame.K_RIGHT]:
				self.speedx = +5
			if keystate[pygame.K_SPACE]:
				self.shoot()
			self.rect.x += self.speedx
		

		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		
	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet = Bullet(self.rect.centerx, self.rect.top)
			all_sprites.add(bullet)
			player_bullets.add(bullet)
			
	def hide(self):
		self.hidden = True
		self.hide_timer = pygame.time.get_ticks()
		self.rect.center = (WIDTH/2, HEIGHT + 200)
			
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = player_bullet_img
		self.image = pygame.transform.scale(self.image, (20, 20))
		self.rect = self.image.get_rect()
		self.rect.x = x - 9
		self.rect.y = y - 10
		self.speedy = -4
		self.radius = int(self.rect.width/4)

		
	def update(self):
		self.rect.y += self.speedy
		if self.rect.y < 0:
			self.kill()
		

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)		
		
		

class Aliens(pygame.sprite.Sprite):
	def __init__(self, x, y, enemy_type):
		pygame.sprite.Sprite.__init__(self)
		self.enemy_type = enemy_type
		filename = 'enemy{}.png'.format(self.enemy_type)
		img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
		self.image = img
		self.image = pygame.transform.scale(self.image, (16, 16))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.speedx = 1
		self.radius = int(self.rect.width/2)
		self.score = 10
		for self in enemies:
			if self.enemy_type == 1:
				self.score = 10
			elif self.enemy_type == 2:
				self.score = 50
			elif self.enemy_type == 3:
				self.score == 100

		
	def update(self):
		self.rect.x += self.speedx
		if self.rect.x > WIDTH - 15:
			self.rect.x = WIDTH - 15
			for self in enemies:
				self.speedx *= -1
				self.rect.y += 10
				
		if self.rect.x < 0:
			self.rect.x = 0
			for self in enemies:
				self.speedx *= -1
				self.rect.y += 10
				
	def shoot(self):
		bullet = EnemyBullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		enemy_bullets.add(bullet)

		
class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_bullet_img
		self.image = pygame.transform.scale(self.image, (20, 30))
		self.rect = self.image.get_rect()
		self.rect.x = x - 9
		self.rect.y = y - 10
		self.speedy = 4
		self.radius = int(self.rect.width/4)
		
	def update(self):
		self.rect.y += self.speedy
		if self.rect.y > 600:
			self.kill()


clock = pygame.time.Clock()

def game_loop():
	probability = 0.0004
	running = True
	
	enemyCount = len(aliens.sprites())
	aliensDead = 0
	#while running == True:
	while running:
		clock.tick(FPS)
		#draw/ display
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
		
		for enemy in enemies:
			fireChance = random.random()
			
			if(fireChance <= probability):
			
				x = enemy.rect.x
				y = enemy.rect.y
				enemy_bullet = EnemyBullet(x, y)
				enemy_bullets.add(enemy_bullet)
				enemy.shoot()
			if enemy.rect.y > player.rect.bottom:
				for bullet in player_bullets:
					bullet.kill()
				for bullet in enemy_bullets:
					bullet.kill()
				for alien in aliens:
					alien.kill()
				enemies.clear()
				player.hide()
				level(-1)
				score(-1)
				running = False
				pygame.wait(100)
				screen.fill(BLACK)
				draw_text(screen, "GAME OVER", 64, WIDTH/2, HEIGHT/6, YELLOW)
				draw_text(screen, "loading...", 40, WIDTH/2, HEIGHT/2 - 40, RED)
				pygame.display.flip()
				pygame.time.wait(100)
				break
		for alien in aliens:
			hits = pygame.sprite.spritecollide(alien, player_bullets, True, pygame.sprite.collide_circle)
			for hit in hits:
				score(alien.score)
				all_sprites.remove(alien)
				enemies.remove(alien)
				aliens.remove(alien)
				hit.kill()
				aliensDead += 1
				if aliensDead == enemyCount/2:
					for alien in aliens:
						alien.speedx *= 2
						probability = 0.00070
				if aliensDead == (3*enemyCount)/4:
					for alien in aliens:
						alien.speedx *= 3/2
						probability = 0.0030
				if aliensDead == enemyCount -1:
					for alien in aliens:
						alien.speedx *= 5/3
						probability = 0.0200
				
				if not enemies:
					for bullet in enemy_bullets:
						bullet.kill()
					for bullet in player_bullets:
						bullet.kill()
					level_change()
					
			
					
		hits = pygame.sprite.spritecollide(player, aliens, False, pygame.sprite.collide_circle)
		if hits:
			for bullet in player_bullets:
				bullet.kill()
			for bullet in enemy_bullets:
				bullet.kill()
			for alien in aliens:
				alien.kill()
			enemies.clear()
			player.hide()
			level(-1)
			score(-1)
			running = False
			pygame.wait(100)
			screen.fill(BLACK)
			draw_text(screen, "GAME OVER", 64, WIDTH/2, HEIGHT/6, YELLOW)
			draw_text(screen, "loading...", 40, WIDTH/2, HEIGHT/2 - 40, RED)
			pygame.display.flip()
			pygame.time.wait(100)
			break
		hits = pygame.sprite.spritecollide(player, enemy_bullets, False, pygame.sprite.collide_circle)
		if hits:
			player.hide()
			player.lives -= 1
		if  player.lives <= 0:
			for bullet in player_bullets:
				bullet.kill()
			for bullet in enemy_bullets:
				bullet.kill()
			for alien in aliens:
				alien.kill()
			enemies.clear()
			player.hide()
			level(-1)
			score(-1)
			running = False
			pygame.time.wait(100)
			screen.fill(BLACK)
			draw_text(screen, "GAME OVER", 64, WIDTH/2, HEIGHT/6, YELLOW)
			draw_text(screen, "loading...", 40, WIDTH/2, HEIGHT/2 - 40, RED)
			pygame.display.flip()
			pygame.time.wait(100)
			break
		
		
		screen.blit(background, (0,0))
		all_sprites.update()
		draw_text(screen, "Score: " + str(int(score(0))), 20, WIDTH/2, 10, WHITE)
		draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
		all_sprites.draw(screen)
		
		pygame.display.flip()

while(True):
	all_sprites = pygame.sprite.Group()
	player = Player()
	all_sprites.add(player)
	aliens = pygame.sprite.Group()
	make_Enemies()
	player_bullets = pygame.sprite.Group()
	enemy_bullets = pygame.sprite.Group()
	game_loop()