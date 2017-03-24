from mcp23017_lib import Adafruit_MCP230XX
import time

#mcp_butt = Adafruit_MCP230XX(busnum = 1, address = 0x22, num_gpios = 16)
#mcp_led = Adafruit_MCP230XX(busnum = 1, address = 0x24, num_gpios = 16)
mcp_pres = Adafruit_MCP230XX(busnum = 1, address = 0x23, num_gpios = 16)
OUTPUT = 0
INPUT = 1

for i in range(8):
	print "input - " +  str(i)
	mcp_pres.config(i, INPUT)

for i in range(8):
	print "output - " +  str(i+8)
	mcp_pres.config(i+8, OUTPUT)

#while True:
#	for i in range(16):
#		#j =  i+8
#		if(mcp_butt.input(i)):
#			mcp_led.output(i, 1)
#			print(i)
#		else:
#			mcp_led.output(i, 0)

while True:	
	for i in range(8):
		if mcp_pres.input(i):
			print i
			mcp_pres.output(i+8, 1)
		else:
			mcp_pres.output(i+8, 0)
	#mcp_pres.output(i+8, 1)
	#time.sleep(1)
	#mcp_pres.output(i+8, 0)
	#time.sleep(1)