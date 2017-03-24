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
	for i in range(2):
		screen.addstr(y+1+i, x+1, s[i] +  str(levels[i]) + " "*(3-len(str(levels[i]))))

	for i in range(2):
		screen.addstr(y+1+i, x+7, s[i] +  str(levels[i]) + " "*(3-len(str(levels[i]))))

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

#if int(width) < 130:
#	width = 130

#if int(height) < 41:
#	hwight = 41

wId = int(width)/10
hId = int(height)/8

poses = []

class DMX_screen(object):
	def __init__(self, uiData, bankData):
		if int(width) >= 130 and int(height) >= 41:

			uiData = json.loads(uiData)
			bankData = json.loads(bankData)

			i = 0
			j = 0
			num = 1
			level = [0,0,0,0]
			for i in range(8):
#				for j in range(2):
				if uiData["lamSel"][num-1] == 1:
					drawRect(0*wId+1,i*hId+1, int(wId), int(hId), str(num) + " SEL")
				else:
					drawRect(0*wId+1,i*hId+1, int(wId), int(hId), str(num))

				pos = [0*wId+1,i*hId+1]

				poses.append(pos)

				level[0] = uiData["lamp"+str(num)]["r"]
				level[1] = uiData["lamp"+str(num)]["g"]
				level[2] = uiData["lamp"+str(num)]["b"]
				level[3] = uiData["lamp"+str(num)]["l"]

				setButText(0*wId+1,i*hId+1, level)


				if uiData["lamSel"][num+7] == 1:
					drawRect(wId+1,i*hId+1, int(wId), int(hId), str(num+8) + " SEL")
				else:
					drawRect(wId+1,i*hId+1, int(wId), int(hId), str(num+8))

				pos = [1*wId+1,i*hId+1]

				poses.append(pos)

				level[0] = uiData["lamp"+str(num+7)]["r"]
				level[1] = uiData["lamp"+str(num+7)]["g"]
				level[2] = uiData["lamp"+str(num+7)]["b"]
				level[3] = uiData["lamp"+str(num+7)]["l"]

				setButText(1*wId+1,i*hId+1, level)

				num +=1


			drawRect(2*wId + 3, 1, 11*4-1, 3, -1)
			
			for i in range(4):
				a = int(2*wId+(i)*8+(i+1)*3)
				drawRect(a, 3, 10, 3, -1)
				screen.addstr(4, a+1, str(uiData["pot"][i]))
				screen.refresh()

			screen.addstr(7, 2*wId + 3, "Bank: " + str(uiData["bank"]))
			screen.refresh()

			for i in range(8):
				lev = uiData["dmxCh"][i]

				potBox(2*wId+(7+3)*i + 3, 12, 7, int(height)-13, lev, i+1)

			#screen.addstr(2, int(width)-30, "width: " + width)
			#screen.addstr(3, int(width)-30, "height: " + height)

		else:
			screen.addstr(1,1, "Screen too small!")

		screen.refresh()

	def updatePot(self, potId, level):
		if int(width) >= 130 and int(height) >= 41:
			potBox(2*wId+(7+3)*(potId-1) + 3, 12, 7, int(height)-13, level, potId) 

			screen.addstr(2, int(width)-30, "")

		else:
			screen.addstr(1,1, "Screen too small!")

		screen.refresh()

	def updateSel(self, id, state):
		if int(width) >= 130 and int(height) >= 41:
			if state == 1:
				drawRect(poses[id-1][0], poses[id-1][1], int(wId), int(hId), str(id) + " SEL")
			else:
				drawRect(poses[id-1][0], poses[id-1][1], int(wId), int(hId), str(id))

			screen.addstr(2, int(width)-30, "")

		else:
			screen.addstr(1,1, "Screen too small!")

		screen.refresh()

	def updateLampData(self, id, levels):
		if int(width) >= 130 and int(height) >= 41:
			setButText(poses[id-1][0], poses[id-1][1], levels)

			screen.addstr(2, int(width)-30, "")

		else:
			screen.addstr(1,1, "Screen too small!")

		screen.refresh()

	def updateUi(self, uiData, bankData):
		if int(width) >= 130 and int(height) >= 41:
			bankData = json.loads(bankData)
			uiData = json.loads(uiData)

			i = 0
			j = 0
			num = 1
			level = [0,0,0,0]
			for i in range(8):
#				for j in range(2):
				if uiData["lamSel"][num-1] == 1:
					drawRect(0*wId+1,i*hId+1, int(wId), int(hId), str(num) + " SEL")
				else:
					drawRect(0*wId+1,i*hId+1, int(wId), int(hId), str(num))

				pos = [0*wId+1,i*hId+1]

				poses.append(pos)

				level[0] = uiData["lamp"+str(num)]["r"]
				level[1] = uiData["lamp"+str(num)]["g"]
				level[2] = uiData["lamp"+str(num)]["b"]
				level[3] = uiData["lamp"+str(num)]["l"]

				setButText(0*wId+1,i*hId+1, level)


				if uiData["lamSel"][num+7] == 1:
					drawRect(wId+1,i*hId+1, int(wId), int(hId), str(num+8) + " SEL")
				else:
					drawRect(wId+1,i*hId+1, int(wId), int(hId), str(num+8))

				pos = [1*wId+1,i*hId+1]

				poses.append(pos)

				level[0] = uiData["lamp"+str(num+7)]["r"]
				level[1] = uiData["lamp"+str(num+7)]["g"]
				level[2] = uiData["lamp"+str(num+7)]["b"]
				level[3] = uiData["lamp"+str(num+7)]["l"]

				setButText(1*wId+1,i*hId+1, level)

				num +=1

			#drawRect(2*wId + 3, 1, 11*4-1, 3, -1)
			
			for i in range(4):
				a = int(2*wId+(i)*8+(i+1)*3)
				#asd=str(uiData["pot" + str(i+1)]["color"])
				#drawRect(a, 3, 10, 3, str(uiData["pot"+str(i+1)]["color"]).upper())
				screen.addstr(4, a+1, str(uiData["pot"][i]) + " "*(4-len(str(uiData["pot"][i]))))
				screen.refresh()

			screen.addstr(7, 2*wId + 3, "Bank: " + str(uiData["bank"]))
			screen.refresh()

			for i in range(8):
				lev = uiData["dmxCh"][i]

				potBox(2*wId+(7+3)*i + 3, 12, 7, int(height)-13, lev, i+1)

		else:
			screen.addstr(1,1, "Screen too small!")

		screen.refresh()

	def cleanup(self):
		curses.echo()
		curses.nocbreak()
		curses.curs_set(2)
		curses.endwin()


if __name__ == "__main__":
	try:
		scr = DMX_screen(open('server/lamps.json'), open('server/data.json'))

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