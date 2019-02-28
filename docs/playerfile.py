import itertools
import requests
import os
import re

class Player:
		
	def __init__(self, name, position):
			
		self.name = name
		self.role = position
		self.lcsteam = None
		self.ffteam = None
		self.one = [0 for x in range(0,20)] 		# Kills or Towers
		self.two = [0 for x in range(0,20)] 		# Deaths or Inhibitors
		self.three = [0 for x in range(0,20)]	 	# Assists or Barons
		self.four = [0 for x in range(0,20)]		# Creep Score or Dragons
		self.five = [0 for x in range(0,20)] 		# Gold or Rift Heralds
		self.score = [0 for x in range(0,10)]
		self.record = [0,0]
		

	# Player type modifiers
	def get_name(self):
		return self.name
	def get_roster(self):
		return self.ffteam or 'no one'
	def add_one(self, value, spot):
		self.one[spot]= value
	def add_two(self, value, spot):
		self.two[spot]= value
	def add_three(self, value, spot):
		self.three[spot]= value
	def add_four(self, value , spot):
		self.four[spot]= value
	def add_five(self,value, spot):
		self.five[spot]= value
	def team_win(self):
		self.record[0] += 1
	def team_loss(self):
		self.record[1] += 1
	def get_record(self):
		if self.role == 'Team':
			return self.record
		else:
			print('This dude is a PLAYER not a TEAM')
	def update_score(self):
		for x in range(0,20):	
			if self.role == 'Support':
				self.score[x//2] = round(float(self.one[x]) - float(self.two[x]) + float(self.three[x]) + float(self.five[x])*0.1, 2)
			else:
				self.score[x//2] = round(float(self.one[x]) - float(self.two[x]) + float(self.three[x])*0.5 + float(self.four[x])*0.01 + float(self.five[x])*0.1, 2)
	def get_score(self):
		return self.score

class User:

	def __init__(self, user_name, team_name):
		self.user_name = user_name
		self.team_name = team_name
		self.roster = [None for x in range(0, 8)] # 8 Total Slots
		self.record = [0, 0]
		self.starters = [None for x in range(0, 6)] # Lane Lane Jng Supp Team

	def get_user(self):
		return self.user_name
	def get_teamname(self):
		return self.team_name
	def get_starters(self):
		for x in self.starters:
			try:	
				print(f"{x.name}")
			except AttributeError as e:
				print('No one here')
	def starter_swap(self, p, r):
		assert r in self.roster
		assert p in self.roster
		if p not in self.starters and r in self.starters:
			lanespot = ['Top', 'Mid']
			if (p.role == r.role) or (p.role in lanespot and r.role in lanespot):
				self.starters[self.starters.index(r)] = p
			else:
				print(f'{p.name} cannot be placed in this spot')
		else:
			print(f'Yo this dude {r.get_name()} is NOT in your starting lineup ')
	def start_player(self, p):
		# Places player in correct roster spot if available
		if p in self.roster and p not in self.starters:
			spot =[]
			if p.role == 'Top' or p.role == 'Mid':
				spot.append(0)
				spot.append(1)
			elif p.role == 'Jungler':
				spot.append(2)
			elif p.role == 'Bot':
				spot.append(3)
			elif p.role == 'Support':
				spot.append(4)
			elif p.role == 'Team':
				spot.append(5)
			else:
				print(f'{p.role} is not currently defined, somethins fucky')
			placed = False
			for x in spot:
				if self.starters[x] == None:
					self.starters[x] = p
					placed = True
					break
			if not placed:
				print('Starting lineup is currently full')

	def bench_player(self, p):
		assert p in self.starters
		self.starters[self.starters.index(p)] = None


	def replace_player(self, p, r):
		# Finds Player Object r in roster and replaces it with Player Object p
		self.waiver_player(r)
		self.update_roster(p)
		self.roster[self.roster.index(r)] = p
	def trade_player(self, p, p2, team2):
		assert len(self.roster) <= 8
		self.roster[self.roster.index(p)] = p2
		team2.roster[team2.roster.index(p2)] = p
		p.ffteam =  team2.team_name
		p2.ffteam = self.team_name

	def add_player(self, p):
		assert len(self.roster) <= 8
		if p.ffteam == None:
			assert None in self.roster
			Found = False
			for count in range(0, len(self.roster)):
				if Found:
					break
				if self.roster[count] == None:
					self.update_roster(p)
					self.roster[count] = p
					Found = True
			assert len(self.roster) == 8
		else:
			print(f'{p.name} is already on team {p.get_roster()}')

	def update_roster(self, p):
		assert len(self.roster) <= 8
		p.ffteam = self.team_name

	def waiver_player(self, p):
		assert len(self.roster) <= 8
		try: 
			p.ffteam = None
		except AttributeError as e:
			print(f'Something got weird')
	def user_win(self):
		self.record[0] += 1
	def user_loss(self):
		self.record[1]+=1
	def get_record(self):
		return self.record

