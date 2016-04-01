from os import system
import warnings

import time
from keys import uk, aid

import speech_recognition as sr
from pb_py import main as API

import csv

import ngram

from chatterbot import ChatBot

bot = ChatBot("Terminal",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapters=[
        "chatterbot.adapters.logic.EvaluateMathematically",
        "chatterbot.adapters.logic.TimeLogicAdapter",
        "chatterbot.adapters.logic.ClosestMatchAdapter"
    ],
    io_adapters=[
        "chatterbot.adapters.io.TerminalAdapter"
    ],
    database="../database.db")

bot.train("chatterbot.corpus.english")

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
	# Some basic data cleaning
	bot_response = bot_response.replace("'", "")
	bot_response = bot_response.replace("\n", "")
	bot_response = bot_response.replace("(", "")
	bot_response = bot_response.replace(")", "")
	bot_response = bot_response.replace(";", "")
	print("Pyggy said: " + bot_response)
	system("say -v Fiona -r 180 " + bot_response)
	

# obtain audio from the microphone	
warnings.filterwarnings("ignore")
r = sr.Recognizer()

# lm = ngram.train_char_lm("sonnets.txt", order=12)
# short_sonnet = ngram.generate_text(lm, 12, nletters=200)

timenow = time.time()
with open('logs/' + str(timenow) + '_log.csv', 'wb') as csvfile:
	with sr.Microphone() as source:
		# r.adjust_for_ambient_noise(source)
		writer = csv.writer(csvfile)
		fieldnames = ['timestamp', 'input_text', 'response']
		writer.writerow(fieldnames)
		opener = "What is your name?"
		# speak_response(opener)
		while True:
			bot_input = bot.get_response(opener)
			# audio = r.listen(source)
			try:
				# input_text = r.recognize_google(audio)
				print("You said: " + input_text)
				result = API.talk(user_key, app_id, host, botname, input_text, session_id=True, recent=True)
				response = result['response']
				writer.writerow([time.time(),input_text,response])
				csvfile.flush()
				# speak_response(response)
				# time.sleep(0.1)
			except:
				pass
			
			
# The problem with the nmaive bot is it is determined and focused.
# Generative n-grams have no context to help the program to generate an appropriate word next
# There is no solution provided by one for the other.
# there must be some kind of stance generated for the robot over the course of the robot
# number of words used in a day, linguistics studies about daily word usage.
# average daily vocabulary





