# import pygame
import math
import numpy as np
import time

from main import main 	#TODO we might actually want to rly separate GUI and game cause it'll be easier to see AIs play 
# from GUI import MainWindow

# screen_width = 1500
# screen_height = 800
# check_point = ((1200, 660), (1250, 120), (190, 200), (1030, 270), (250, 475), (650, 690))

class Car:
	def __init__(self, car_file, map_file, pos):
		pass
		# self.surface = pygame.image.load(car_file)
		# self.map = pygame.image.load(map_file)
		# self.surface = pygame.transform.scale(self.surface, (100, 100))
		# self.rotate_surface = self.surface
		# self.pos = pos
		# self.angle = 0
		# self.speed = 0
		# self.center = [self.pos[0] + 50, self.pos[1] + 50]
		# self.radars = []
		# self.radars_for_draw = []
		# self.is_alive = True
		# self.current_check = 0
		# self.prev_distance = 0
		# self.cur_distance = 0
		# self.goal = False
		# self.check_flag = False
		# self.distance = 0
		# self.time_spent = 0
		# for d in range(-90, 120, 45):
		# 	self.check_radar(d)

		# for d in range(-90, 120, 45):
		# 	self.check_radar_for_draw(d)

	# def draw(self, screen):
	# 	screen.blit(self.rotate_surface, self.pos)

	# def draw_collision(self, screen):
	# 	for i in range(4):
	# 		x = int(self.four_points[i][0])
	# 		y = int(self.four_points[i][1])
	# 		pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)

	# def draw_radar(self, screen):
	# 	for r in self.radars_for_draw:
	# 		pos, dist = r
	# 		pygame.draw.line(screen, (0, 255, 0), self.center, pos, 1)
	# 		pygame.draw.circle(screen, (0, 255, 0), pos, 5)

	# def check_collision(self):
	# 	self.is_alive = True
	# 	for p in self.four_points:
	# 		if self.map.get_at((int(p[0]), int(p[1]))) == (255, 255, 255, 255):
	# 			self.is_alive = False
	# 			break

	# def check_radar(self, degree):
	# 	len = 0
	# 	x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
	# 	y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

	# 	while not self.map.get_at((x, y)) == (255, 255, 255, 255) and len < 300:
	# 		len = len + 1
	# 		x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
	# 		y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

	# 	dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
	# 	self.radars.append([(x, y), dist])

	# def check_radar_for_draw(self, degree):
	# 	len = 0
	# 	x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
	# 	y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

	# 	while not self.map.get_at((x, y)) == (255, 255, 255, 255) and len < 300:
	# 		len = len + 1
	# 		x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
	# 		y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

	# 	dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
	# 	self.radars_for_draw.append([(x, y), dist])

	# def check_checkpoint(self):
	# 	p = check_point[self.current_check]
	# 	self.prev_distance = self.cur_distance
	# 	dist = get_distance(p, self.center)
	# 	if dist < 70:
	# 		self.current_check += 1
	# 		self.prev_distance = 9999
	# 		self.check_flag = True
	# 		if self.current_check >= len(check_point):
	# 			self.current_check = 0
	# 			self.goal = True
	# 		else:
	# 			self.goal = False

	# 	self.cur_distance = dist

	# def update(self):
	# 	#check speed
	# 	self.speed -= 0.5
	# 	if self.speed > 10:
	# 		self.speed = 10
	# 	if self.speed < 1:
	# 		self.speed = 1

	# 	#check position
	# 	self.rotate_surface = rot_center(self.surface, self.angle)
	# 	self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
	# 	if self.pos[0] < 20:
	# 		self.pos[0] = 20
	# 	elif self.pos[0] > screen_width - 120:
	# 		self.pos[0] = screen_width - 120

	# 	self.distance += self.speed
	# 	self.time_spent += 1
	# 	self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
	# 	if self.pos[1] < 20:
	# 		self.pos[1] = 20
	# 	elif self.pos[1] > screen_height - 120:
	# 		self.pos[1] = screen_height - 120

	# 	# caculate 4 collision points
	# 	self.center = [int(self.pos[0]) + 50, int(self.pos[1]) + 50]
	# 	len = 40
	# 	left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * len]
	# 	right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * len]
	# 	left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * len]
	# 	right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * len]
	# 	self.four_points = [left_top, right_top, left_bottom, right_bottom]


class PyGame2D:
	def __init__(self, speed):
		# pygame.init()
		self.game = main()
		self.game_speed = speed
		# self.gui = 
		# self.mode = 0

	def action(self, action):
		#TODO actually rather than that i think we should use GUI left etc ?
		if action == 0:
			self.game.left()
		elif action == 1:
			self.game.right()
		elif action == 2:
			self.game.up()
		elif action == 3:
			self.game.down()
		
		time.sleep(self.game_speed)

	def evaluate(self):
		reward = 0
		smooth_weight = 5
		mono_weight = 10
		non_z_weight = 0.01 #50
		max_weight = 0

		matrix = self.game.matrix

		if self.game.u_dead_yet() == -1:
			#if you lost that's bad but not that bad if you manage to go quite far
			# ? Do we want to keep such a condition actually ?
			reward = -1e18 + self.game.score
		elif self.game.u_dead_yet() == 1:
			#if you won now that's great !
			reward = 1e18
		
		#increase reward based on max number on the board
		maxi = np.max(matrix)

		#reward for smoothness
		smoothness = 0
		for i in range(4):
			for j in range(4):
				if matrix[i,j]:
					value = np.log(matrix[i,j]) / np.log(2) if matrix[i,j] != 0 else 1
					for direction in np.array([[1,0], [0, 1]]):
						vector = direction
						k,l = i,j
						# print("qdqzd")
						while (k<3 and l<3) and (matrix[k,l] != 0):
								k += direction[0]
								l += direction[1]

						if matrix[k,l] != 0:
							target = np.log(matrix[k,l]) / np.log(2)
							smoothness += np.abs(value - target)
		
		#reward for monolithic boards
		mono = 0
		totals = [0, 0, 0, 0]

		# up/down direction
		for x in range(4):
			current = 0
			nextc = current+1
			while nextc<4:
				while nextc<4 and matrix[x,nextc] != 0:
					nextc += 1

				if nextc >= 4: nextc -= 1
				currentValue = np.log(matrix[x][current]) / np.log(2) if matrix[x,current] != 0 else 0
				nextcValue = np.log(matrix[x][nextc]) / np.log(2) if matrix[x,nextc] != 0 else 0

				if currentValue > nextcValue:
					totals[0] += nextcValue - currentValue
				elif nextcValue > currentValue:
					totals[1] += currentValue - nextcValue
				
				current = nextc
				nextc += 1
		
		# left/right direction
		for y in range(4):
			current = 0
			nextc = current+1
			while nextc<4:
				while nextc<4 and matrix[nextc,y] != 0:
					nextc += 1

				if nextc >= 4: nextc -= 1
				currentValue = np.log(matrix[current,y]) / np.log(2) if matrix[current,y] != 0 else 0
				nextcValue = np.log(matrix[nextc,y]) / np.log(2) if matrix[nextc,y] != 0 else 0

				if currentValue > nextcValue:
					totals[2] += nextcValue - currentValue
				elif nextcValue > currentValue:
					totals[3] += currentValue - nextcValue
				
				current = nextc
				nextc += 1
				
		mono = max(totals[0], totals[1]) + max(totals[2], totals[3])

		#penalty for too few empty tiles
		non_z = np.count_nonzero(matrix)

		# check if max is in one of the corners
		# max_index = np.unravel_index(np.argmax(matrix), (4,4))
		# if (max_index[0] == 0 or max_index[0] == 3) and (max_index[1] == 0 or max_index[1] == 3):
		# 	max_pos_weight = 1000
		# else: max_pos_weight = 0
		max_pos_weight = 0

		m = np.ones((4,4))
		for i in range(4):
			for j in range(4):
				if i % 2 == 0:
					m[i,j] *= (15-i-j)
				else: m[i,3-j] *= (15-i-3+j)
				# 	m[i,j] = 0.1**(i+j)
				# else: m[i,3-j] = 0.1**(i+3-j)
				# 	m[i,j] = 2**(15-i-j)
				# else: m[i,3-j] = 2**(15-i-3+j)
		return 1e-4 * np.sum(matrix * m) - non_z_weight * non_z
		
		# #TOTAL
		# reward += mono_weight * mono + max_weight * maxi - smooth_weight * smoothness - non_z_weight * non_z + max_pos_weight
		# return reward

	def is_done(self):
		#TODO add condition to prevent pressing 200 times left and nothing happening maybe ?
		if self.game.u_dead_yet() == 0:
			return False #then the game continues
		return True #then u won / lost so maybe u should restart episode

	def observe(self):
		# ? TODO could be like score, maxi, [i,j] of maxi, ?? what else ?
		max_index = np.unravel_index(np.argmax(self.game.matrix), (4,4))
		obs = [int(np.count_nonzero(self.game.matrix)), int(np.count_nonzero(self.game.score)), int(np.max(self.game.matrix)), max_index[0], max_index[1]]
		# obs = list(self.game.matrix.flatten().astype(np.int))

		return tuple(obs) #TODO change the dimension where this function is called as well as where the Box observation space is defined

	def view(self):
		pass
		# print(self.game.matrix)
		#TODO this is where we want the GUI to update i guess ?
		#TODO it should update automatically just as long as we specifiy GUI.left rather than game.left in the action method i guess ?
		# # draw game

