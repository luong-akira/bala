import pygame,sys
import random,math
pygame.init()
#VARIABLES
track_movement = 0
cactus_list = []
jump_force = 5
gravity = 1
ready_to_jump = True
game_active = True
move_down = False
bird_list =[]
score = 0
highest_score = 0
isCrounching = False
reset_key_hd = False

#LOAD IMAGES
screen = pygame.display.set_mode((1200,800))
icon = pygame.image.load('dino_runner.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Dino Runner")
clock = pygame.time.Clock()
track = pygame.image.load("Other/Track.png").convert_alpha()
#LOAD FONTS
game_font = pygame.font.Font('04B_19.ttf', 40)
# DINO RUN
dino_run1 = pygame.image.load("Dino/DinoRun1.png").convert_alpha()
dino_run2 = pygame.image.load("Dino/DinoRun2.png").convert_alpha()
dino_jump =  pygame.image.load("Dino/DinoJump.png").convert_alpha()
dino_duck1 = pygame.image.load("Dino/DinoDuck1.png").convert_alpha()
dino_duck2 = pygame.image.load("Dino/DinoDuck2.png").convert_alpha()
dino_run_frames = [dino_run1,dino_run2]
dino_run_index = 0
dino = dino_run_frames[dino_run_index]
# DINO
dino_duck_frames = [dino_duck1,dino_duck2]
dino_duck_index = 0
dino_duck = dino_duck_frames[dino_duck_index]
dino_run_rect = dino.get_rect(center = (75,725))
dino_duck_rect = dino_duck.get_rect(center=(75,750))
# CACTUS
Large_Cactus1 = pygame.image.load("Cactus/LargeCactus1.png").convert_alpha()
Large_Cactus2 = pygame.image.load("Cactus/LargeCactus2.png").convert_alpha()
Large_Cactus3 = pygame.image.load("Cactus/LargeCactus3.png").convert_alpha()
large_cactus = [Large_Cactus1,Large_Cactus2,Large_Cactus3]
Large_Cactus1_rect = Large_Cactus1.get_rect(center=(600,720))
# BIRD
Bird_1 = pygame.image.load("Bird/Bird1.png").convert_alpha()
Bird_2 = pygame.image.load("Bird/Bird2.png").convert_alpha()
Bird_frames = [Bird_1,Bird_2]
Bird_index = 0
Bird = Bird_frames[Bird_index]
Bird_rect = Bird.get_rect(center = (75,670))
#CLOUD
Cloud = pygame.image.load("Other/Cloud.png").convert_alpha()
Cloud_rect = Cloud.get_rect(center=(600,200))
# USEREVENT
SPAWNCACTUS = pygame.USEREVENT
RUNNING  = pygame.USEREVENT + 1
SPAWNBIRD = pygame.USEREVENT + 2
BIRD_ANM = pygame.USEREVENT + 3 
pygame.time.set_timer(RUNNING, 100)
pygame.time.set_timer(SPAWNCACTUS, random.randint(1200,2000))
pygame.time.set_timer(SPAWNBIRD, random.randint(4000, 8000))
pygame.time.set_timer(BIRD_ANM, 400)

#FUNCTIONS

def score_display():
	score_surface = game_font.render("Score: "+str(int(score/10)), True, (0,0,0))
	score_rect = score_surface.get_rect(center=(600,50))
	heightest_score_surface = game_font.render(str(int(score)), True, (0,0,0))
	height_score_rect = heightest_score_surface.get_rect(center=(500,700))
	screen.blit(score_surface, score_rect)
	#screen.blit(heightest_score_surface,height_score_rect)
def create_cactus():
	global chosed_cactus
	chosed_cactus = random.choice(large_cactus)
	choosed_cactus_rect = chosed_cactus.get_rect(center=(1200,720))
	return choosed_cactus_rect
def move_cactus(cactuses):
	for cactus in cactuses:		
		cactus.centerx -= 2
	return cactuses
def draw_cactus(cactuses):
	for cactus in cactuses:
		screen.blit(chosed_cactus, cactus)

def dino_run_animation():
	new_dino = dino_run_frames[dino_run_index]
	new_dino_run_rect = new_dino.get_rect(center=(75,dino_run_rect.centery))
	return new_dino, new_dino_run_rect

def dino_duck_animation():
	new_dino_duck = dino_duck_frames[dino_duck_index]
	new_dino_duck_rect = new_dino_duck.get_rect(center=(75,dino_duck_rect.centery))
	return new_dino_duck, new_dino_duck_rect
def create_bird():
	#new_bird = bird_frames[bird_index]
	new_bird_rect = Bird_1.get_rect(center =(1100,Bird_rect.centery))
	return new_bird_rect
def move_bird(birds):
	for bird in birds:
		bird.centerx-=1
	return birds
def draw_birds(birds):
	for bird in birds:
		screen.blit(bird_animation(), bird)
def bird_animation():
	new_bird = Bird_frames[Bird_index]
	return new_bird

def check_cactuses_collision(cactuses):
	for cactus in cactuses:
		if dino_run_rect.colliderect(cactus):
			return False
def check_birds_collision(birds):
	for bird in birds:
		if isCrounching == True:
			if dino_duck_rect.colliderect(bird):
				return False
		elif isCrounching == False:
			if dino_run_rect.colliderect(bird):
				return False


class Game_state():
	def __init__(self):
		self.state = 'intro'
	def intro(self):
		screen.fill((255,255,255))
		play_button = game_font.render("Please Press Space To Play", True, (0,0,0))
		play_rect = play_button.get_rect(center=(600,400))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.state = 'main_game'

		screen.blit(play_button,play_rect)
		pygame.display.update()
	def scene_management(self):
		if self.state == 'intro':
			self.intro()
		elif self.state == 'main_game':
			self.main_game()
		elif self.state == 'reset':
			self.reset()
	def reset(self):
		global game_active
		global score
		screen.fill((255,255,255))
		reset_button = pygame.image.load("Other/Reset.png")
		reset_button_rect = reset_button.get_rect(center=(600,400))
		screen.blit(reset_button, reset_button_rect)
		score_display()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed(num_buttons=3):
					x,y = pygame.mouse.get_pos()
					if 350< y < 450 and 563 <x<637 :
						print(reset_button_rect.bottomleft[1])					
						game_active = True
						self.state = 'main_game'
						bird_list.clear()
						cactus_list.clear()
						score = 0
		pygame.display.update()
	def main_game(self):
		global track_movement
		global cactus_list
		global jump_force 
		global gravity 
		global ready_to_jump 
		global game_active 
		global move_down
		global bird_list 
		global score 
		global dino_run_rect
		global dino
		global dino_run_index
		global Bird_index
		global dino_duck_index
		global isCrounching
		screen.fill((255,255,255))
		for event in pygame.event.get():
			if event.type == pygame.QUIT: #or game_active == False:
				pygame.quit()
				sys.exit()
			if game_active == False:
				self.state = 'reset'
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and ready_to_jump:
					dino_run_rect.centery -= jump_force * 60				
				if event.key == pygame.K_DOWN:
					move_down = True
					isCrounching = True					
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_DOWN:
					move_down = False
					isCrounching = False
			if event.type == SPAWNCACTUS:	
				cactus_list.append(create_cactus())
				if len(cactus_list) == 4 :
					cactus_list.pop(1)	
						
			if event.type == RUNNING:
				if dino_run_index > 0:
					dino_run_index = 0
				else:
					dino_run_index += 1					
				dino, dino_run_rect = dino_run_animation()

			if event.type == SPAWNBIRD:
				bird_list.append(create_bird())
				if len(bird_list) == 4:
					bird_list.pop(1)

			if event.type == BIRD_ANM:
				if Bird_index > 0:
					Bird_index = 0
				else:
					Bird_index += 1
		if game_active:

			track_movement-= 0.1
			if track_movement < -1200:
				track_movement = 0

			dino_run_rect.centery += gravity
			if dino_run_rect.centery > 725:
				dino_run_rect.centery = 725
			if dino_run_rect.centery == 725: # ON THE GROUND
				ready_to_jump = True
				if move_down: # KEY IS BEING HOLD DOWN 
					if dino_duck_index > 0:
						dino_duck_index = 0
					else:
						dino_duck_index += 1
					#print("key is being hold")
					dino_duck , dino_duck_rect = dino_duck_animation()
					screen.blit(dino_duck, dino_duck_rect)
				else:
					screen.blit(dino, dino_run_rect)
			else: # ON THE AIR 
				screen.blit(dino_jump, dino_run_rect)
				ready_to_jump = False
				
			bird_list = move_bird(bird_list)
			draw_birds(bird_list)

			cactus_list = move_cactus(cactus_list)
			screen.blit(track, (track_movement,750))	
			screen.blit(Cloud, (track_movement,200))
			screen.blit(Cloud, (track_movement-1000,200))
			draw_cactus(cactus_list)
			check_collision_1 = check_cactuses_collision(cactus_list)
			check_collision_2 = check_birds_collision(bird_list)
			if check_collision_1 == False or check_collision_2 == False:
				game_active = False
			if game_active:
				score += 0.1

				score_display()
			

		pygame.display.update()

game_state = Game_state()

while True:
	game_state.scene_management()