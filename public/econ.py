from playerfile import Player
from playerfile import User
from pstats import get_match_id, get_match, get_game_stats
import os
import itertools
import requests
import json
# All imports from roster.py
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
import time
import re
import multiprocessing as mp 
from multiprocessing import Process, current_process, Queue
from operator import itemgetter


# Full 2019 LCS Roster
_100Thieves = Player('100Thieves', 'Team')
Ssumday = Player('Ssumday', 'Top')
AnDa = Player('AnDa', 'Jungler')
huhi = Player('huhi', 'Mid')
Bang = Player('Bang', 'Bot')
aphromoo = Player('aphromoo', 'Support')
Ryu = Player('Ryu', 'Coach')

Cloud9 = Player('Cloud9', 'Team')
Licorice = Player('Licorice', 'Top')
Blaber = Player('Blaber', 'Jungler')
Svenskeren = Player('Svenskeren', 'Jungler')
Goldenglue = Player('Goldenglue', 'Mid')
Nisqy = Player('Nisqy', 'Mid')
Sneaky = Player('Sneaky', 'Bot')
Zeyzal = Player('Zeyzal', 'Support')
RapidStar = Player('RapidStar', 'Coach')

ClutchGaming = Player('ClutchGaming', 'Team')
Huni = Player('Huni', 'Top')
Lira = Player('Lira', 'Jungler')
Damonte = Player('Damonte', 'Mid')
Piglet = Player('Piglet', 'Bot')
Vulcan = Player('Vulcan', 'Support')

CounterLogicGaming = Player('CounterLogicGaming', 'Team')
Darshan = Player('Darshan', 'Top')
FallenBandit = Player('FallenBandit', 'Top')
Moon = Player('Moon', 'Jungler')
Wiggily = Player('Wiggily', 'Jungler')
PowerOfEvil = Player('PowerOfEvil', 'Mid')
Stixxay = Player('Stixxay', 'Bot')
Biofrost = Player('Biofrost', 'Support')

EchoFox = Player('EchoFox', 'Team')
Solo = Player('Solo', 'Top')
Rush = Player('Rush', 'Jungler')
Fenix = Player('Fenix', 'Mid')
Apollo = Player('Apollo', 'Bot')
Hakuho = Player('Hakuho', 'Support')

FlyQuest = Player('FlyQuest', 'Team')
V1per = Player('V1per', 'Top')
Santorin = Player('Santorin', 'Jungler')
Pobelter = Player('Pobelter', 'Mid')
WildTurtle = Player('WildTurtle', 'Bot')
JayJ = Player('JayJ', 'Support')

GoldenGuardians = Player('GoldenGuardians', 'Team')
Hauntzer = Player('Hauntzer', 'Top')
Contractz = Player('Contractz', 'Jungler')
Froggen = Player('Froggen', 'Mid')
deftly = Player('deftly', 'Bot')
Olleh = Player('Olleh', 'Support')

OpTicGaming = Player('OpTicGaming', 'Team')
Allorim = Player('Allorim', 'Top')
Dhokla = Player('Dhokla', 'Top')
Dardoch = Player('Dardoch', 'Jungler')
Meteos = Player('Meteos', 'Jungler')
Crown = Player('Crown', 'Mid')
Arrow = Player('Arrow', 'Bot')
Asta = Player('Asta', 'Bot')
BIG = Player('BIG', 'Support')
Gate = Player('Gate', 'Support')

TeamLiquid = Player('TeamLiquid', 'Team')
Impact = Player('Impact', 'Top')
Xmithie = Player('Xmithie', 'Jungler')
Jensen = Player('Jensen', 'Mid')
Doublelift = Player('Doublelift', 'Bot')
CoreJJ = Player('CoreJJ', 'Support')
TF_blade = Player('TF blade', 'Coach')

TeamSoloMid = Player('TeamSoloMid', 'Team')
Broken_blade = Player('Broken blade', 'Top')
Akaadian = Player('Akaadian', 'Jungler')
Bjergsen = Player('Bjergsen', 'Mid')
Zven = Player('Zven', 'Bot')
Smoothie = Player('Smoothie', 'Support')
Lustboy = Player('Lustboy', 'Coach')


def update_players(stats):
	imports = "os", "re"
	# Finds the output queue and updates player scores automatically
	for a in stats:
		if a[1]:
			spot = (a[0] - 1) // 5 # Makes sure that each week has two days of 5 games
			for b in a[1]:
				for c in b:
					if c and len(c)>2:
						try:
							special_name = c[0].split(' ')[1]

							if special_name == 'Broken':
								special_name = 'Broken_blade'
								
							elif special_name == 'Big':
								special_name = 'BIG'
								

							elif special_name == 'Deftly':
								special_name = 'deftly'

							
							eval(special_name).lcsteam = c[0].split(' ')[0]
							eval(special_name).add_one(c[1], spot)
							eval(special_name).add_two(c[2], spot)
							eval(special_name).add_three(c[3], spot)
							eval(special_name).add_four(c[4], spot)
							eval(special_name).add_five(c[5][:-1], spot)
							
						except IndexError as e:
							pass



def update_data(players):
	with open("players.json", "w") as write_file:
		data = {}
		data['players'] = []
		for player in players:
			data['players'].append({
				'name': player.get_name(), 
				'ffteam' : player.get_roster(),
				'lcsteam' : player.lcsteam,
				'role': player.role, 
				'score': [],
				'stats' : {
					'kills': player.one, 
					'deaths': player.two, 
					'assists': player.three, 
					'cs': player.four, 
					'gold': player.five
				}
			})
		json.dump(data, write_file, indent=4, separators=(',', ':'))


def update_teams(teams):
	with open("teams.json", "w") as write_file:
		data = {}
		data['ffteams'] = []
		for team in teams:
			ros = []
			for a in team.roster:
				try:
					ros.append(a.get_name())
				except AttributeError as e:
					ros.append('none')
			star = []
			for a in team.starters:
				try:
					star.append(a.get_name())
				except AttributeError as e:
					star.append('none')
			data['ffteams'].append({
				'name' : team.get_user(),
				'team_name' : team.get_teamname(),
				'stats' : {
					'roster': ros,
					'record': team.record,
					'starters': star
				}
			})
		json.dump(data, write_file, indent=4, separators=(',', ':'))


# Econ 2019 Fantasy LCS Spring Split

# Full Econ User Roster
team_one = User('TeaEye', 'BjergsendNudes')
team_two = User('Nickolishus', 'Yagami')
team_three = User('tylerkungpao', 'pls gank mid')
team_four = User('Ronster', 'Zvend Nudes')
team_five = User('Jacob', 'Sike')
#team_six = User('Christian', 'OnePeas')

# Draft

# ~~~~~~~~~ Round 1 ~~~~~~~~~
team_one.add_player(Bjergsen)
team_two.add_player(Doublelift)
team_three.add_player(Jensen)
team_four.add_player(Zven)
team_five.add_player(Sneaky)
#team_six.add_player()

# ~~~~~~~~~ Round 2 ~~~~~~~~~
team_one.add_player(Apollo)
team_two.add_player(Bang)
team_three.add_player(WildTurtle)
team_four.add_player(huhi)
team_five.add_player(Crown)
#team_six.add_player()

# ~~~~~~~~~ Round 3 ~~~~~~~~~
team_one.add_player(Pobelter)
team_two.add_player(Fenix)
team_three.add_player(Damonte)
team_four.add_player(PowerOfEvil)
team_five.add_player(Nisqy)
#team_six.add_player()

# ~~~~~~~~~ Round 4 ~~~~~~~~~
team_one.add_player(Stixxay)
team_two.add_player(Huni)
team_three.add_player(CoreJJ)
team_four.add_player(Licorice)
team_five.add_player(Xmithie)
#team_six.add_player()

# ~~~~~~~~~ Round 5 ~~~~~~~~~
team_one.add_player(Svenskeren)
team_two.add_player(Rush)
team_three.add_player(Santorin)
team_four.add_player(AnDa)
team_five.add_player(V1per)
#team_six.add_player()

# ~~~~~~~~~ Round 6 ~~~~~~~~~
team_one.add_player(Ssumday)
team_two.add_player(Zeyzal)
team_three.add_player(TeamLiquid)
team_four.add_player(aphromoo)
team_five.add_player(Impact)
#team_six.add_player()

# ~~~~~~~~~ Round 7 ~~~~~~~~~
team_one.add_player(Cloud9)
team_two.add_player(TeamSoloMid)
team_three.add_player(Piglet)
team_four.add_player(_100Thieves)
team_five.add_player(JayJ)
#team_six.add_player()

# ~~~~~~~~~ Round 8 ~~~~~~~~~
team_one.add_player(Smoothie)
team_two.add_player(Broken_blade)
team_three.add_player(Hauntzer)
team_four.add_player(Arrow)
team_five.add_player(ClutchGaming)
#team_six.add_player()

teams = [team_one, team_two, team_three, team_four, team_five]
players = [Impact, Xmithie, Jensen, Doublelift, CoreJJ, TF_blade, Ssumday, AnDa, huhi, Bang, aphromoo, Licorice, Svenskeren, Blaber, Goldenglue, Nisqy, Sneaky, Zeyzal, Huni, Lira, Damonte, Piglet, Vulcan, Darshan, FallenBandit, Moon, Wiggily, PowerOfEvil, Stixxay, Biofrost, Solo, Rush, Fenix, Apollo, Hakuho, V1per, Santorin, Pobelter, WildTurtle, JayJ, Hauntzer, Contractz, Froggen, deftly, Olleh, Allorim, Dhokla, Dardoch, Meteos, Crown, Arrow, Asta, BIG, Gate, Broken_blade, Akaadian, Bjergsen, Zven, Smoothie]

s_stats = get_game_stats(get_match_id('https://lol.gamepedia.com/LCS/2019_Season/Spring_Season'))
update_players(s_stats)

for p in players:
	p.update_score()

update_data(players)
update_teams(teams)