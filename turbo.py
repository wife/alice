from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import winsound
import bs4 as bs
import urllib.request
import time
import termcolor
import os
import sys
from requests import get
import pyfiglet
import colorama
from colorama import Fore, Back, Style
from colorama import init
colorama.init()
init(strip=not sys.stdout.isatty())
from termcolor import cprint 
from pyfiglet import figlet_format
cprint(figlet_format('dove.rip', font='lean'),
       'red', 'on_grey', attrs=['bold'])

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=125x125")
prefs = {"profile.managed_default_content_settings.images":2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("http://steamcommunity.com/profiles/76561198447338200/edit")

User = input("user: ")
Pass = input("pass: ")
frequency = 100
duration = 1000
requests = 0

error = "Steam Community :: Error"

driver.find_element_by_id("steamAccountName").send_keys(User)
driver.find_element_by_id("steamPassword").send_keys(Pass)
driver.find_element_by_id("SteamLogin").click()
for i in range(3, 0, -1):
	print("Logging in..." + "(" + str(i) + ")", end="\r", flush=True),
	time.sleep(1)
try:
	element = WebDriverWait(driver, 0).until(
	EC.presence_of_element_located((By.ID, "authcode")))
	print("Auth code found!")
	authcode = input("auth code: ")
	driver.find_element_by_xpath("""//*[@id="twofactorcode_entry"]""").send_keys(authcode)
	driver.find_element_by_xpath("""//*[@id="twofactorcode_entry"]""").send_keys(u'\ue007')
except TimeoutException:
	print("no auth code")

ID = input("id to fish: ")
print(Style.RESET_ALL + "Now fishing for " + Fore.CYAN + ID + Style.RESET_ALL + "!")
driver.find_element_by_id("customURL").clear()
while True:
	try:
		url = urllib.request.urlopen("http://steamcommunity.com/id/" + ID + "/videos")
		soup = bs.BeautifulSoup(url, 'html.parser')
		availability = soup.title.string
		requests = requests + 1
		print(requests, end='\r')
		if availability == error:
			driver.find_element_by_id("customURL").send_keys(ID)
			driver.find_element_by_id("customURL").send_keys(u'\ue007')
			customURLcheck = driver.find_element_by_id("customURL").get_attribute('value')
			if customURLcheck == ID:
				print(Fore.GREEN + "You fished " + ID + "!")
				winsound.Beep(frequency, duration)
				sys.exit()
	except urllib.error.HTTPError as e:
		if e.code == 503:
			print("Error code 503! Refreshing.")
	except Exception:
		print("Exception caught!")