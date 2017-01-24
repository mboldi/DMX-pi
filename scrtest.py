from screen import DMX_screen
import time
from random import randint

try:
	scr = DMX_screen(open('lamps.json'), open('server/data.json'))

	scr.updatePot(1, 255)
	time.sleep(1)
	scr.updatePot(1, 0)

	scr.updateLampData(1, [randint(0,255), randint(0,255), randint(0,255), randint(0,255),])

	time.sleep(5)
finally:
	scr.cleanup()