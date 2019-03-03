from bs4 import BeautifulSoup
import urllib
import mechanicalsoup
import itertools
import requests
import os
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
import time
import re
import multiprocessing as mp 
from multiprocessing import Process, current_process, Queue
from operator import itemgetter

# Created by: Jacob Arriola
# E-mail: Jarriola2012@gmail.com
# Input: gamepedia tournament page
# Output: Match stats for all game

def get_match_id(page):

	# Input: Lol Gamepedia Tournament URL Page
	# Output: All matchhistory pages if available 
	# Isolates match history links on page

	req = urllib.request.Request(page, headers={'User-Agent' : "Magic Browser:"})
	con = urllib.request.urlopen( req )
	soup = BeautifulSoup(con, "html.parser")
	temp = soup.select('.mdv-allweeks')
	matches=[[] for x in range(0,10)]
	for z in temp:
		if "column-label-small" not in z.get('class') and 'TBD' not in z: # and "toggle" not in str(z.get('class')):
			try:
				week = z.get('class')[1]
				week = int(re.search(r'\d+', week).group())
				_MH = "N/A"
				for b in z:
					for c in b:
						if "matchhistory" in str(c):
							_MH = c.get('href')
							_MH = _MH.replace('euw', 'na')
				matches[week-1].append(_MH)
			except AttributeError as e:
				pass
	return matches

def get_match(match_id,x,output):
	# Input: URL as string for League of Legends Match History
	# Output: Match Data [10[Team+Player, Kills, Deaths, Assists, CS, Gold]] + 2[Baron, Dragons, Turrets, Inhibitors]
	# Isolates relevant stats based on classes and removes unnecesarry strings
	nogame = None
	# If match history is unavailable stats are uploaded as N/A. Can be swapped with actual stats manually
	if match_id == 'N/A':
		output.put((x, nogame))
	else:
		chromeOptions = webdriver.ChromeOptions()
		prefs={"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
		chromeOptions.add_experimental_option("prefs", prefs)
		chrome_options = Options()  
		chrome_options.add_argument("--headless") 
		driver = webdriver.Chrome(chrome_options=chromeOptions)
		driver.implicitly_wait(10)
		try :
			print(f"Processing game {x}:")
			driver.set_page_load_timeout(120) # Following ensures pages are loaded correctly and no data is lost
			driver.get(match_id)
			driver.refresh()
			SCROLL_PAUSE_TIME = 0.1
			SCROLL_LENGTH = 250
			page_height = int(driver.execute_script("return document.body.scrollHeight"))
			scrollPosition = 0
		# Scroll to bottom of page. Driver is designed to wait until window scrolls to bottom to exit driver
			while scrollPosition < page_height:
				scrollPosition += SCROLL_LENGTH
				driver.execute_script("window.scrollTo(0, " + str(scrollPosition) + ");")
				time.sleep(SCROLL_PAUSE_TIME)
			soup = BeautifulSoup(driver.page_source, "html.parser")
			driver.quit()

		except TimeoutException as e:

			print("Page load Timeout Occured. Quiting !!!")
			driver.quit()

		# Miscellaneous data magic to get player results and team results
		player_r =[a for a in (x.select('.binding')for x in soup.select('.classic.player')) if a]

		results = []
		for a in player_r:
			for b in a:
				if 'item-icon' not in b.attrs['class'] and 'spell-icon' not in b.attrs['class'] and 'champion-icon' not in b.attrs['class']:
					results.append(b.get_text())
		p_results = [results[i:i+7] for i in range(0, len(results), 7)]
		for a in p_results:
			a.pop(0)
		team_r = soup.select('.classic.team-footer')
		t_results = [[],[]]
		count=0
		for b in team_r:
			t_results[count].append(re.findall("\d+", b.get_text()))
			count+=1
		output.put((x, [p_results, t_results]))
		print(f"Finished game {x}")


def get_game_stats(season):
	output = mp.Queue()
	lcs_season = season
	procs = []
	results= []
	count = 0
	print("---------- Beginning data extraction ----------")
	for week in lcs_season:
		for game in week:
			count+= 1
			proc = Process(target=get_match, args=(game, count, output))
			procs.append(proc)
			proc.start()
		for x in range(0,len(week)):
			results.append(output.get())
		proc.join()
	results = sorted(results, key=itemgetter(0))
	print("---------- Finished data extraction ----------")
	return results
