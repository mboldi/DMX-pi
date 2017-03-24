import sys
import time
from rotary_lib import RotaryEncoder
# Define GPIO inputs
PIN_A = [17, 27, 23, 25, 12] # Pin 8
PIN_B = [4, 18, 22, 24, 5] # Pin 10
BUTTON = [6, 13, 19, 16, 26] # Pin 7
# This is the event callback routine to handle events
def switch0_event(event):
	if event == RotaryEncoder.CLOCKWISE:
		print "Clockwise0"
	elif event == RotaryEncoder.ANTICLOCKWISE:
		print "Anticlockwise0"
	elif event == RotaryEncoder.BUTTONDOWN:
		print "Button down0"
	elif event == RotaryEncoder.BUTTONUP:
		print "Button up0"
	return

def switch1_event(event):
	if event == RotaryEncoder.CLOCKWISE:
		print "Clockwise1"
	elif event == RotaryEncoder.ANTICLOCKWISE:
		print "Anticlockwise1"
	elif event == RotaryEncoder.BUTTONDOWN:
		print "Button down1"
	elif event == RotaryEncoder.BUTTONUP:
		print "Button up1"
	return

def switch2_event(event):
	if event == RotaryEncoder.CLOCKWISE:
		print "Clockwise2"
	elif event == RotaryEncoder.ANTICLOCKWISE:
		print "Anticlockwise2"
	elif event == RotaryEncoder.BUTTONDOWN:
		print "Button down2"
	elif event == RotaryEncoder.BUTTONUP:
		print "Button up2"
	return
	
def switch3_event(event):
	if event == RotaryEncoder.CLOCKWISE:
		print "Clockwise3"
	elif event == RotaryEncoder.ANTICLOCKWISE:
		print "Anticlockwise3"
	elif event == RotaryEncoder.BUTTONDOWN:
		print "Button down3"
	elif event == RotaryEncoder.BUTTONUP:
		print "Button up3"
	return
	
def switch4_event(event):
	if event == RotaryEncoder.CLOCKWISE:
		print "Clockwise4"
	elif event == RotaryEncoder.ANTICLOCKWISE:
		print "Anticlockwise4"
	elif event == RotaryEncoder.BUTTONDOWN:
		print "Button down4"
	elif event == RotaryEncoder.BUTTONUP:
		print "Button up4"
	return
# Define the switch
rswitch0 = RotaryEncoder(PIN_A[0],PIN_B[0],BUTTON[0],switch0_event)
rswitch1 = RotaryEncoder(PIN_A[1],PIN_B[1],BUTTON[1],switch1_event)
rswitch2 = RotaryEncoder(PIN_A[2],PIN_B[2],BUTTON[2],switch2_event)
rswitch3 = RotaryEncoder(PIN_A[3],PIN_B[3],BUTTON[3],switch3_event)
rswitch4 = RotaryEncoder(PIN_A[4],PIN_B[4],BUTTON[4],switch4_event)
while True:
 time.sleep(0.5)