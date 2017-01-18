import curses
import os
import json
import time

width = 0
height = 0

screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)

def mapp(value, imin, imax, jmin, jmax):
	return (value - imin) * (jmax - jmin) // (imax - imin) + jmin

def drawRect(x, y, w, h, id):
	if id != -1:
		q = 0
		for q in range(w -2):
			screen.addstr(y, x+q +1, "-")

		q = 0
		for q in range(w -2):
			screen.addstr(y+h-1, x+q+1, "-")

		q = 0
		for q in range(h):
			screen.addstr(y+q, x, "|")

		q = 0
		for q in range(h):
			screen.addstr(y + q, x + w-1, "|")

		screen.addstr(y, x + (w-len(str(id)))/2, str(id))
	else:
		q = 0
		for q in range(w -2):
			screen.addstr(y, x+q +1, "-")

		q = 0
		for q in range(w -2):
			screen.addstr(y+h-1, x+q+1, "-")

		q = 0
		for q in range(h):
			screen.addstr(y+q, x, "|")

		q = 0
		for q in range(h):
			screen.addstr(y + q, x + w-1, "|")

	screen.refresh()

def setButText(x, y, levels):
	i = 0
	s = ["R=", "G=", "B=", "LUM="]
	for i in range(4):
		screen.addstr(y+1+i, x+1, s[i] +  str(levels[i]) + " "*(3-len(str(levels[i]))))

	screen.refresh()

def potBox(x, y, w, h, level, id):
	q = 0
	for q in range(w -2):
		screen.addstr(y, x+q +1, "-")

	q = 0
	for q in range(w -2):
		screen.addstr(y+h-1, x+q+1, "-")

	q = 0
	for q in range(h):
		screen.addstr(y+q, x, "|")

	q = 0
	for q in range(h):
		screen.addstr(y + q, x + w-1, "|")

	drawRect(x, y-3, w, 3, "Pre" + str(id))

	screen.addstr(y-2, x+1 , str(level) + " "*(4-len(str(level))))

	up = 1
	l=0
	while(l <= h-2):
		if(l <= mapp(level, 0, 255, 0, h-2)):
			screen.addstr(y+h-up-1, int(x+w/2), "H")
		else:
			screen.addstr(y+h-up, int(x+w/2), " ")

		up += 1
		l += 1

	screen.refresh()

height, width = os.popen('stty size', 'r').read().split()
wId = int(width)/12
hId = int(height)/8

poses = []

class DMX_screen(object):
	def __init__(self, lamps, ui):

		lampData = json.load(lamps)
		uiData = json.load(ui)

		i = 0
		j = 0
		num = 1
		level = [0,0,0,0]
		for i in range(8):
			for j in range(2):
				if uiData["lamSel"]["State" + str(num)] == 1:
					drawRect(j*wId+1,i*hId+1, int(wId), int(hId), str(num) + " SEL")
				else:
					drawRect(j*wId+1,i*hId+1, int(wId), int(hId), str(num))

				pos = [j*wId+1,i*hId+1]

				poses.append(pos)

				level[0] = lampData["lamp"+str(num)]["r"]
				level[1] = lampData["lamp"+str(num)]["g"]
				level[2] = lampData["lamp"+str(num)]["b"]
				level[3] = lampData["lamp"+str(num)]["l"]

				setButText(j*wId+1,i*hId+1, level)

				num +=1


		drawRect(2*wId + 3, 1, 11*4-1, 3, -1)
		
		for i in range(4):
			a = int(2*wId+(i)*8+(i+1)*3)
			asd=str(uiData["pot" + str(i+1)]["color"])
			drawRect(a, 3, 10, 3, str(uiData["pot"+str(i+1)]["color"]).upper())
			screen.addstr(4, a+1, str(uiData["pot" + str(i+1)]["level"]))
			screen.refresh()

		screen.addstr(7, 2*wId + 3, "Bank: " + str(1))
		screen.refresh()

		for i in range(4):
			lev = uiData["pot" + str(i+1)]["level"]

			potBox(2*wId+(7+3)*i + 3, 12, 7, int(height)-13, lev, i+1)

	def updatePot(self, potId, level):
		potBox(2*wId+(7+3)*(potId-1) + 3, 12, 7, int(height)-13, level, potId) 

	def updateSel(self, id, state):
		if state == 1:
			drawRect(poses[id-1][0], poses[id-1][1], int(wId), int(hId), str(id) + " SEL")
		else:
			drawRect(poses[id-1][0], poses[id-1][1], int(wId), int(hId), str(id))

	def updateLampData(self, id, levels):
		setButText(poses[id-1][0], poses[id-1][1], levels)

	def cleanup(self):
		curses.echo()
		curses.nocbreak()
		curses.endwin()


if __name__ == "__main__":
	try:
		scr = DMX_screen(open('lamps.json'), open('server/data.json'))

		for i in range(255):
			scr.updatePot(1, i)
			time.sleep(0.01)

		scr.updatePot(1, 255)
		time.sleep(0.01)

		while (i >= 0):
			scr.updatePot(1, i)
			i -= 1
			time.sleep(0.01)

		scr.updatePot(1, 255)
		time.sleep(1)
		scr.updatePot(1, 0)

		scr.updateSel(1, 1)
		time.sleep(1)
		scr.updateSel(1, 0)
		time.sleep(1)
		scr.updateSel(1, 1)

		scr.updateLampData(1, [123,255,45,255])

		time.sleep(5)
	finally:
		#scr.cleanup()
		curses.echo()
		curses.nocbreak()
		curses.curs_set(2)
		curses.endwin()