from os import system
import warnings

import time
from keys import uk, aid

import speech_recognition as sr
from pb_py import main as API

import csv

host = 'aiaas.pandorabots.com'
user_key = uk
app_id = aid
botname = 'pyggy2'

## Diagnostic information

#result = API.list_bots(user_key, app_id, host)
#print result

# for i in os.listdir('pyggy'):
# 	filename = 'pyggy/' + i
# 	result = API.upload_file(user_key, app_id, host, botname, filename)
# 	print result

# result = API.list_files(user_key, app_id, host, botname)
# print result

# result = API.compile_bot(user_key, app_id, host, botname)
# print result

def speak_response(response):
	bot_response = response
	bot_response = bot_response.replace("'", "")
	system("say -v Fiona -r 160 " + bot_response)
	print("Pyggy said: " + bot_response)

# obtain audio from the microphone	
warnings.filterwarnings("ignore")
r = sr.Recognizer()

timenow = time.time()
with open('logs/' + str(timenow) + '_log.csv', 'wb') as csvfile:
	with sr.Microphone() as source:
		
		# Make sure you handle the ambient noise
		r.adjust_for_ambient_noise(source)
		writer = csv.writer(csvfile)
		fieldnames = ['timestamp', 'input_text', 'response']
		writer.writerow(fieldnames)
		opener = "Let's start with your name..."
		speak_response(opener)
		while True:
			audio = r.listen(source)
			input_text = r.recognize_google(audio)
			print("You said: " + input_text)
			result = API.talk(user_key, app_id, host, botname, input_text, session_id=True, recent=True)
			response = result['response']
			writer.writerow([time.time(),input_text,response])
			csvfile.flush()
			speak_response(response)
			time.sleep(0.1)
			
			





