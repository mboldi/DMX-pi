import time
import os
import RPi.GPIO as gpio
import json
import sys

gpio.setmode(gpio.BCM)
DEBUG = 1

ledPin = 5
potPin = 0

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

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
gpio.setup(SPIMOSI, gpio.OUT)
gpio.setup(SPIMISO, gpio.IN)
gpio.setup(SPICLK, gpio.OUT)
gpio.setup(SPICS, gpio.OUT)

gpio.setup(ledPin, gpio.OUT)

while True:
	pot = readadc(potPin, SPICLK, SPIMOSI, SPIMISO, SPICS)
	pot = mapp(pot, 1, 1023, 0, 255)

	with open('/home/pi/DMX-pi/server/data.json') as json_data:
		data = json.load(json_data)
		gpio.output(ledPin, data["lamSel"]["State1"])


	sys.stdout.write("\r " + str(pot) + "   ")
	sys.stdout.flush()
	time.sleep(0.1)