import time
import os
import RPi.GPIO as gpio
import json
import sys
import curses
from mcp23017_lib import Adafruit_MCP230XX
from screen import DMX_screen
import shlex, subprocess
import requests

gpio.setmode(gpio.BCM)
DEBUG = 1

mcp_butt = Adafruit_MCP230XX(busnum = 1, address = 0x22, num_gpios = 16)
mcp_led = Adafruit_MCP230XX(busnum = 1, address = 0x24, num_gpios = 16)
OUTPUT = 0
INPUT = 1

#I2C pins
ledPin = 0
butPin = 1

#SPI pins
potPin = 0

for i in range(16):
	mcp_butt.config(i, INPUT)
	mcp_led.config(i, OUTPUT)

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
	   if ((adcnum > 7) or (adcnum < 0)):
			 return -1
	   gpio.output(cspin, True)

	   gpio.output(clockpin, False)  # start clock low
	   gpio.output(cspin, False)     # bring CS low

	   commandout = adcnum
	   commandout |= 0x18  # start bit + single-ended bit
	   commandout <<= 3    # we only need to send 5 bits here
	   for i in range(5):
			 if (commandout & 0x80):
				    gpio.output(mosipin, True)
			 else:
				    gpio.output(mosipin, False)
			 commandout <<= 1
			 gpio.output(clockpin, True)
			 gpio.output(clockpin, False)

	   adcout = 0
	   # read in one empty bit, one null bit and 10 ADC bits
	   for i in range(12):
			 gpio.output(clockpin, True)
			 gpio.output(clockpin, False)
			 adcout <<= 1
			 if (gpio.input(misopin)):
				    adcout |= 0x1

	   gpio.output(cspin, True)
	   
	   adcout >>= 1       # first bit is 'null' so drop it
	   return adcout

def mapp(value, imin, imax, jmin, jmax):
	return (value - imin) * (jmax - jmin) // (imax - imin) + jmin

def request(urlEnd, lastReq):
	if((time.time()-lastReq) >= 0.05):
		try: #ha nincs meg a data.json, akkor atmasolja a backup fajlbol, ha megvan, akkor forditva
			with open('server/data.json') as data:
				json.loads(data)
				os.system('cp server/data.json backup_data.json')
		except:
			os.system('cp backup_data.json server/data.json')

		requests.get('http://localhost:8081/' + str(urlEnd))
		lastReq = time.time()
		return lastReq
	else:
		return lastReq

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 11 #18
SPIMISO = 9 #23
SPIMOSI = 10 #24
SPICS = 8 #25

# set up the SPI interface pins
gpio.setup(SPIMOSI, gpio.OUT)
gpio.setup(SPIMISO, gpio.IN)
gpio.setup(SPICLK, gpio.OUT)
gpio.setup(SPICS, gpio.OUT)

#gpio.setup(ledPin, gpio.OUT)
#gpio.setup(butPin, gpio.IN)

wasChange = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

try:
	#start server
	sStart_script = shlex.split('sudo node server/index.js')
	server = subprocess.Popen(sStart_script)
	time.sleep(5)

	os.system('curl http://localhost:8081/init')

	time.sleep(0.5)

	resp = requests.get('http://localhost:8081/bankdata')
	#print resp.text
	bankdata = json.loads(resp.text)

	#for i in range(16):
	#	state[i] = uiJson["lamSel"]["State" + str(i+1)]

	lastUpd = time.time()

	scr = DMX_screen(requests.get('http://localhost:8081/uidata').text, requests.get('http://localhost:8081/bankdata').text)

	potLast = 0
	lastUpd = 0
	lastReq = 0

	while True:
		pot = readadc(potPin, SPICLK, SPIMOSI, SPIMISO, SPICS)
		pot = mapp(pot, 0, 1023, 0, 255)

		#update data
		if (time.time()-lastUpd) >= 0.01:
			uidata = requests.get('http://localhost:8081/uidata').text
			bankdata = requests.get('http://localhost:8081/bankdata').text

			scr.updateUi(uidata, bankdata)

			uiJson = json.loads(uidata)
			bankJson = json.loads(bankdata)

			for i in range(16):
				#name = "State" + str(i+1)
				state[i] = int(uiJson["lamSel"][i])

			lastUpd = time.time()
			#lastReq = time.time()

		if pot != potLast:
			#scr.updatePot(1, pot)
			requests.get('http://localhost:8081/updatedmxch/0/' + str(pot))
			potLast = pot
			lastReq = time.time()

		for i in range(16):
			if mcp_butt.input(i) and wasChange[i] == 0:
				if state[i] == 0:
					state[i] = 1
				else:
					state[i] = 0
				scr.updateSel(1, state[i])

				mcp_led.output(i, 1)

				state[i] = int(requests.get('http://localhost:8081/updateSel/' + str(i)).text)

				wasChange[i] = 1
			elif not mcp_butt.input(i):
				wasChange[i] = 0

		for i in range(16):
			mcp_led.output(i, state[i])

		time.sleep(0.01)

finally:
	gpio.cleanup()
	try:
		scr.cleanup()
	except:
		curses.echo()
		curses.nocbreak()
		curses.curs_set(2)
		curses.endwin()

	server.terminate()