
import curses
import time

def screenrefr(i):
	stdscr.addstr(0,0, "I erteke: " + str(i))
	stdscr.addstr(3, 0, "asd " + str(i))
	stdscr.refresh()

if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

i = 0

try:
	for i in range(50):
		i += 1

		screenrefr(i)

		time.sleep(0.1)
finally:
	curses.echo()
	curses.nocbreak()
	curses.endwin()