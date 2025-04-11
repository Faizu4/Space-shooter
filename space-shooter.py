import pygame
import sys
import random
import copy
import math

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Space Shooter game")
#pygame characteristics
info = pygame.display.Info()
width, height = info.current_w, info.current_h
print(f"width: {width}, height: {height}")
screen = pygame.display.set_mode((width,height))
font = pygame.font.SysFont(None, 100)
border_size = 60
clock = pygame.time.Clock()
fps = 60
block_size = 60
hitbox = 0 #0 is False and 1 is True

#loading images
try:
	background_1 =  pygame.image.load('images/background_1.jpeg')
	background_2 = pygame.image.load('images/background_2.jpeg')
	player_spaceship_1 = pygame.image.load('images/player_spaceship_1.png')
	enemy_spaceship = pygame.image.load('images/enemy_spaceship.png')	
	boss_spaceship = pygame.image.load('images/boss.png')
	boss_bullet_img = pygame.image.load("images/boss_bullet.png")
	explosion_img = pygame.image.load("images/explosion.png")
except FileNotFoundError as e:
	print(f'image not found: {e}')
	
#loading sounds
try:
	bullet_sound = pygame.mixer.Sound("sounds/bullet_sound.mp3")
	#bullet_sound_2 = pygame.mixer.Sound("")
	#bullet_sound.set_volume(0.5)
	explosion_sound = pygame.mixer.Sound("sounds/explosion.mp3")
	explosion_sound.set_volume(1.0)
except FileNotFoundError as e:
	print(f"Sound not found: {e}")
	

#player characteristics
spaceship_pos_x = width//2- 100
spaceship_pos_y = 1800
spaceship_size =  60
player_health = 100
health_bar_fixed = 100
player_health_cooldown = 0
player_rect = pygame.Rect(spaceship_pos_x, spaceship_pos_y, 190, 190)
#player_health = player_health//player_health*100
player = True
player_spaceship_1 = player_spaceship_1.subsurface(pygame.Rect(190,115, 190,190))
#player bullet
bullet_width = 15
bullet_height = 20
bullet_pos_x = spaceship_pos_x + 50
bullet_pos_y = spaceship_pos_y
bullet_sleep_time = 0
bullet_speed = 35
player_bullet_strength = 10
bullet_list = []


#boss
boss_pos_x = 180
boss_pos_y = -600
boss_wave_num = 10
#boss health
boss_left_wing_health = 200
boss_right_wing_health = 200
boss_body_health = 300
#boss rect's'
boss_spaceship = boss_spaceship.subsurface(pygame.Rect(0,0, 370, 370))
boss_spaceship = pygame.transform.scale(boss_spaceship, (740,740))
boss_left_wing_rect = pygame.Rect(boss_pos_x, boss_pos_y + 250, 280, 326)
boss_right_wing_rect = pygame.Rect(boss_pos_x + 460, boss_pos_y + 250, 280, 326)
boss_body_rect = pygame.Rect(boss_pos_x + 280, boss_pos_y + 165 , 180, 410)
#boss bullet
boss_bullet_list = []
boss_circular_bullet_list = []
boss_bullet_sleep_time = 0
boss_bullet_rect = pygame.Rect(360, 500, 20, 60)
boss_bullet_img = boss_bullet_img.subsurface(pygame.Rect(40,240, 110,60))
boss_bullet_img = pygame.transform.rotate(boss_bullet_img, 270)

#bot's
spawn_level = -100
enemy_border = 400
enemy_health = 50
bot_health_fixed = 50
bot_health_bar_width = 120
bot_health_bar_width_fixed = 120
bot_health_bar_height = 20
bot_pattern_1 = [
[width//2-100, spawn_level, enemy_health], 
[width//2 - 550, spawn_level - 400, enemy_health], 
[width//2 - 350, spawn_level - 200, enemy_health], 
[width//2 + 150, spawn_level - 200, enemy_health], 
[width//2 + 300, spawn_level -400, enemy_health]]

bot_pattern_2 = [
[width - 300, spawn_level, enemy_health],
[width - 600, spawn_level, enemy_health],
[width - 900, spawn_level, enemy_health]]
#[width - 900, spawn_level, enemy_health],
#[width - 600, spawn_level, enemy_health]]

all_pattern = [bot_pattern_1, bot_pattern_2]
bot_pattern = []
bot_pattern = copy.deepcopy(random.choice(all_pattern))
#bot bullet
bot_bullet_width = 15
bot_bullet_height = 20
bot_bullet_sleep_time = 0
bot_bullet_list = []
bot_bullet_strength = 5

#colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
cyan = (0,255,255)
yellow = (255,255,0)
terracotta = (226,130,101)


#score show
score = 0
score_show = font.render(str(f"Score: {score}"), True, white)
score_rect = score_show.get_rect(center=(170, 170))
#health bar show
health_bar_width = 250
health_bar_height = 80
health_bar_width_fixed = 250
player_health_show = font.render(str(player_health), True, white)
player_health_rect = player_health_show.get_rect(center=(100,80))
#wave show
wave_spawn_time = 10
wave_ready = True
wave_num = 10
wave_num_show = font.render(str(f"Wave {wave_num}"), True, white)
wave_num_rect = wave_num_show.get_rect(center=(width-150, 80))

#game over
game_over = font.render(("Game Over"), True, red)
game_over = pygame.transform.scale(game_over, (800,200))
game_over_rect = game_over.get_rect(center=(width//2, height//2))

#setting background
background = [background_1]
background_y = 0
background_speed = 5
background = random.choice(background)
background = pygame.transform.scale(background , (width, height))


def draw_hitbox(rect):
	if hitbox:
		pygame.draw.rect(screen, green, rect, 5)
	return



while True:
	clock.tick(fps)
	current_time = pygame.time.get_ticks()

	if background_y >= height:
		background_y = 0
	#moving the bullets
	for bullet in bullet_list:
		bullet[1] -= 8
	#moving enemy bullets
	for bullet in bot_bullet_list:
		if wave_num % boss_wave_num != 0:
			bullet[1] += 8
	#moving enemies untill enemy border
	for bot in bot_pattern:
		if wave_num % boss_wave_num != 0 and bot_pattern[0][1] < enemy_border:
				bot[1] += 5
	#player bullet-enemy collision
	if wave_num % boss_wave_num != 0:
		for bot in bot_pattern:
			for bullet in bullet_list:
				player_bullet_rect = pygame.Rect(bullet[0]+100, bullet[1], bullet_width, bullet_height)
				bot_rect = pygame.Rect(bot[0], bot[1], 246, 205)
				
				if player_bullet_rect.colliderect(bot_rect):
					bot[2] -= player_bullet_strength
					bullet_list.remove(bullet)
					if bot[2] <= 0:
						screen.blit(explosion_img, (bot[0], bot[1]))
						score += 50
						pygame.display.flip()
						bot_pattern.remove(bot)
						explosion_sound.play()
				
	#enemy bullet-player collision
	for bullet in bot_bullet_list:
		bullet_rect = pygame.Rect(bullet[0]+115, bullet[1]+100, bot_bullet_width, bot_bullet_height)
		if player_rect.colliderect(bullet_rect) and wave_num % boss_wave_num != 0:
				bot_bullet_list.remove(bullet)
				player_health -= bot_bullet_strength
				player_health_show = font.render(str(player_health), True, white)


	#player-enemy collision
	for bot in bot_pattern:
		bot_rect = pygame.Rect(bot[0], bot[1], 246, 205)
		if player_rect.colliderect(bot_rect) and player_health_cooldown >= 60:
				player_health -= 10
				player_health_cooldown = 0
	' ' ' boss ' ' '
	if wave_num % boss_wave_num == 0:
		if boss_pos_y <= 50:
			boss_pos_y += 10
		
	if boss_pos_y >= 50 and wave_num % boss_wave_num == 0:
		
		#boss rect (hitbox) updating
		boss_left_wing_rect = pygame.Rect(boss_pos_x, boss_pos_y + 250, 280, 326)
		boss_right_wing_rect = pygame.Rect(boss_pos_x + 460, boss_pos_y + 250, 280, 326)
		boss_body_rect = pygame.Rect(boss_pos_x + 280, boss_pos_y + 165 , 180, 410)
		#handling boss elimination
		if boss_left_wing_health <= 0 and boss_right_wing_health <= 0 and boss_body_health <= 0:
			boss_defeated = True
			wave_num += 1
			pygame.time.delay(500)
			boss_pos_x = 180
			boss_pos_y = -600
			
			if current_time - wave_spawn_time > 1000:
				wave_num += 1
				wave_ready = False
			else:
				wave_ready = True
				current_time = wave_spawn_time
			boss_left_wing_health = (wave_num+10)* 10
			boss_right_wing_health = (wave_num+10)*10
			boss_body_health = (wave_num+10) * 20
			
		for bullet in boss_bullet_list:
			#boss bullet rect
			boss_bullet_rect = pygame.Rect(bullet[0]+360, bullet[1]+500, 20, 60)
			#moving boss bullets
			dx = target_x - bullet[0]
			dy = target_y - bullet[1]
			distance = math.hypot(dx, dy)
			if distance != 0:
				dx /= distance
				dy /= distance
			bullet[0] += dx * 5
			bullet[1] += dy * 5
			
			#removing boss bullets if outside the borders
			if bullet[0] < 0 or bullet[0] > width or bullet[1] < 0 or bullet[1] > height:
				boss_bullet_list.remove(bullet)
			
		#adding new boss bullets 
		if boss_bullet_sleep_time >= 60:
			boss_bullet_list.append(([boss_pos_x, boss_pos_y]))
			boss_bullet_sleep_time = 0
			target_x = spaceship_pos_x
			target_y = spaceship_pos_y
		#player boss collision
		if (player_rect.colliderect(boss_body_rect)) or (player_rect.colliderect(boss_left_wing_rect)) or (player_rect.colliderect(boss_right_wing_rect)):
			if player_health_cooldown >= 60:
				player_health -= 20
				player_health_cooldown = 0
		#boss bullet-player collision
		for bullet in boss_bullet_list:
			boss_bullet_rect = pygame.Rect(bullet[0]+360, bullet[1]+500, 20, 60)
			if player_rect.colliderect(boss_bullet_rect):
				player_health -= 10
				boss_bullet_list.remove(bullet)
		#player bullet-boss collision
		for bullet in bullet_list:
			player_bullet_rect = pygame.Rect(bullet[0]+100, bullet[1], bullet_width, bullet_height)
			#left wing collision
			if player_bullet_rect.colliderect(boss_left_wing_rect):
				boss_left_wing_health -= player_bullet_strength
				bullet_list.remove(bullet)
			#right wing collision
			elif player_bullet_rect.colliderect(boss_right_wing_rect):
				boss_right_wing_health -= player_bullet_strength
				bullet_list.remove(bullet)
			#main body collison
			elif player_bullet_rect.colliderect(boss_body_rect):
				boss_body_health -= player_bullet_strength
				bullet_list.remove(bullet)
		
			
			
		
	#if bot list is empty add an random one
	if not bot_pattern and wave_ready and wave_num % boss_wave_num != 0:
		if current_time - wave_spawn_time > 1000:
			bot_pattern = copy.deepcopy(random.choice(all_pattern))
			wave_num += 1
			wave_num_show = font.render(str(f"Wave {wave_num}"), True, white)
			enemy_health += 50
			wave_ready = False
	else:
			wave_ready = True
			wave_spawn_time = current_time
			
			

	#player bullet sleep time
	if bullet_sleep_time >= 90:
		bullet_sleep_time = 0
		bullet_list.append([spaceship_pos_x, spaceship_pos_y])
		#bullet sound
		try:
			bullet_sound.play()
		except:
			pass
	#bot player bullet sleep time
	if bot_bullet_sleep_time >= bullet_speed:
		bot_bullet_sleep_time = 0
		for bot in bot_pattern:
			bot_bullet_list.append([bot[0], bot[1]])
	#removing the bullet if outside the border(player)
	for bullet in bullet_list:
		if bullet[1] < 0:
			bullet_list.remove(bullet)
#	(bot)
	for bullet in bot_bullet_list:
		if bullet[1] > height:
			bot_bullet_list.remove(bullet)
	#handling player dying
	if player_health <= 0:
		bullet_list.clear()
		bot_bullet_list.clear()
		boss_bullet_list.clear()
		bot_pattern.clear()
		wave_num = 1
		
		health_bar_width = 250
		bot_pattern = copy.deepcopy(random.choice(all_pattern))
		
		spaceship_pos_x, spaceship_pos_y = width//2-100, 1800 
		player_rect = pygame.Rect(spaceship_pos_x, spaceship_pos_y, 190, 190)
		player_health = 100
		screen.blit(game_over, game_over_rect)
		pygame.display.update()
		pygame.time.delay(3000)
		
	
	for event in pygame.event.get():
		if event.type == pygame.FINGERDOWN:
			initial_x = event.x * width
			initial_y = event.y * height
			
		if event.type == pygame.FINGERMOTION:
			moving_x = event.x * width
			moving_y = event.y * height
			#moving the player
			spaceship_pos_x += moving_x - initial_x 
			spaceship_pos_y += moving_y - initial_y
	   	#claming so that player remain inside the border
			spaceship_pos_x = max(0, min(width - spaceship_size -130, spaceship_pos_x))
			spaceship_pos_y = max(0, min(height - spaceship_size - 230, spaceship_pos_y))
			#updating player rect
			player_rect = pygame.Rect(spaceship_pos_x, spaceship_pos_y, 190, 190)
			initial_x = moving_x 
			initial_y = moving_y
			#when ship is moving bullet is loading
			bullet_sleep_time += 1
	#regardless of time the bot bullet is loading
	bot_bullet_sleep_time += 1
	boss_bullet_sleep_time += 1
	player_health_cooldown += 1
	background_y += background_speed
	health_bar_width = int(health_bar_width_fixed * (player_health / health_bar_fixed))
			
	#drawings
    #background
	screen.blit(background, (0, background_y))
	screen.blit(background, (0, background_y - height))
	#boss bullets
	for bullet in boss_bullet_list:
		screen.blit(boss_bullet_img, (bullet[0]+360, bullet[1]+500))
		draw_hitbox((bullet[0]+356, bullet[1]+500, 70, 110))
	#bot bullets
	for bullet in bot_bullet_list:
		if wave_num % boss_wave_num != 0:		
			pygame.draw.rect(screen, red, (bullet[0]+115, bullet[1]+100, bot_bullet_width, bot_bullet_height))
		#bot bullet hitbox
		if wave_num % boss_wave_num != 0:
			draw_hitbox((bullet[0]+115, bullet[1]+100, bot_bullet_width, bot_bullet_height))
	for bullets in bullet_list:
		#player bullets
		pygame.draw.rect(screen, red, (bullets[0]+100, bullets[1], bullet_width, bullet_height))
		#player bullets hitboxes
		draw_hitbox((bullets[0]+100, bullets[1], bullet_width, bullet_height))
	try:
		#enemy spaceships
		if wave_num % boss_wave_num != 0:
			for bot in bot_pattern:
				#bot health bar
				bot_health_bar_width = int(bot_health_bar_width_fixed * (bot[2] / bot_health_fixed))
				pygame.draw.rect(screen, red, (bot[0]+60, bot[1]-20, bot_health_bar_width, bot_health_bar_height))
				pygame.draw.rect(screen, white, (bot[0]+60, bot[1]-20, bot_health_bar_width_fixed, bot_health_bar_height), 2)
				#bot drawing
				screen.blit(enemy_spaceship, (bot[0], bot[1]))
				#enemy hitboxes
				draw_hitbox((bot[0], bot[1], 246, 205))
	except NameError:
		#enemy ship is rectangle is img not found
		for bot in bot_pattern:
			pygame.draw.rect(screen, yellow, (bot[0], bot[1], 60, 60))
		#enemy hitboxes
			draw_hitbox((bot[0], bot[1], 246, 205))
	#boss
	if wave_num % boss_wave_num == 0:
		try:
			screen.blit(boss_spaceship, (boss_pos_x, boss_pos_y))
		except NameError:
			pygame.draw.rect(screen, red, (0,0,100,100))
		#left wing
		draw_hitbox((boss_pos_x, boss_pos_y + 250, 280, 326))
		#right wing
		draw_hitbox((boss_pos_x + 460, boss_pos_y + 250, 280, 326))
		#main body
		draw_hitbox((boss_pos_x + 280, boss_pos_y + 165 , 180, 410))
	try:
			#player spaceship
			screen.blit(player_spaceship_1, (spaceship_pos_x, spaceship_pos_y))
 	   	#player spaceship hitbox
			draw_hitbox((spaceship_pos_x, spaceship_pos_y, 190, 190))
	except NameError:
    		#ship is rectangle is img not found
			pygame.draw.rect(screen, white, (spaceship_pos_x, spaceship_pos_y, spaceship_size, spaceship_size))
	    	#rectangle ship hitbox
			draw_hitbox((spaceship_pos_x, spaceship_pos_y, 200,320))
	#health bar
	pygame.draw.rect(screen, green, (40, 40, health_bar_width, health_bar_height))
	pygame.draw.rect(screen, white, (40, 40, health_bar_width_fixed, health_bar_height), 5)
	#wave number
	wave_num_show = font.render(str(f"Wave {wave_num}"), True, white)
	screen.blit(wave_num_show, wave_num_rect)
	#score 
	score_show = font.render(str(f"Score: {score}"), True, white)
	screen.blit(score_show, score_rect)

	pygame.display.flip()
	
pygame.quit()
sys.exit()
