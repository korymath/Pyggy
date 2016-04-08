from os import system
import warnings
import time
from keys import uk, aid
import speech_recognition as sr
from pb_py import main as API
import csv
import ngram
import random
from chatterbot import ChatBot
import ngram
import os.path
import re
import sys
import thread

def spinner():
    while True:
        print '.',
        time.sleep(0.25)

def speak_who(text, name):
	print '\n'
	print name + " said: " + text
	if name == 'Fiona':
		if robotoutput == 'voiceandtext':
			system("say -v Tom -r 250 " + text) 
		return True
	elif name == 'Pyggy':
		if robotoutput == 'voiceandtext':
			system("say -v Samantha -r 250 " + text)
		return True
	else:
		return False

def speak_response(response, name):
	bot_response = response
	# Some basic data cleaning
	bot_response = bot_response.replace("<u>", "")
	bot_response = bot_response.replace("</u>", "")
	bot_response = bot_response.replace("\n", "")
	regex = re.compile('[^a-zA-Z ,.?!]')
	bot_response = regex.sub('', bot_response)
	return speak_who(bot_response, name)

def get_bot_response():
	thread.start_new_thread(spinner, ())
	try:
		result = API.talk(user_key, app_id, host, botname, text1, session_id=True, recent=True)
	except:
		result = "... I could be all wrong... "
	pb_text2 = result['response']

	## When talking with pyggy only respond to the stem
	if userinput == 'bot':
		botresponse2 = bot.get_response(botresponse1)
	else:
		botresponse2 = bot.get_response(text1)

	text2 = pb_text2 + ' ' + botresponse2

	return text2

bot = ChatBot("Pyggy",
    storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",
    logic_adapters=[
        # "chatterbot.adapters.logic.EvaluateMathematically",
        # "chatterbot.adapters.logic.TimeLogicAdapter",
        # "chatterbot.adapters.logic.ClosestMeaningAdapter"
        # closest match seems to work better and faster than the closest meaning
        "chatterbot.adapters.logic.ClosestMatchAdapter"
    ],
    io_adapters=[
        "chatterbot.adapters.io.NoOutputAdapter"
    ],
    database="database_movie_2000_good_new")

## TODO: you have to run mongod for the databse to get rolling.
## 4000 is too slow (1-3 seconds per response)
# But the answers are great, and it doesn't get lost.
## 1000 is about half of a second, could up this to 2000 random conversations. 
## this timing is scaling linearly ,as would be expected.

# check if the database file exists
# if not, then train it
# bot.train("chatterbot.corpus.english.movielines2000rand")

# 16 seconds for 4000 conversation corpuss
# bot.train("chatterbot.corpus.english.conversations")
	
host = 'aiaas.pandorabots.com'
user_key = uk
app_id = aid
botname = 'pyggy2'

# Set some default inputs
if (len(sys.argv) < 2):
	userinput = 'text' # or 'voice' or 'bot'
else:
	userinput = sys.argv[1]

if (len(sys.argv) < 3):
	robotoutput = 'text' # or 'voiceandtext'
else:
	robotoutput = sys.argv[2]

if (len(sys.argv) < 4):
	text1 = "Quick Pyggy, get out of the burning building."
else:
	text1 = sys.argv[3]

# lm = ngram.train_char_lm("pg.txt", order=8)
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

# obtain audio from the microphone	
warnings.filterwarnings("ignore")
r = sr.Recognizer()

timenow = time.time()
with open('logs/' + str(timenow) + '_log.csv', 'wb') as csvfile:
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		writer = csv.writer(csvfile)
		fieldnames = ['timestamp', 'input_text', 'response']
		writer.writerow(fieldnames)
		while True:
			# Dialog starter to come up with text first
			# Human spoken responses
			if userinput == 'voice':
				audio = r.listen(source)
				try:
					text1 = r.recognize_google(audio)
				except:
					text1 = '...something I could not understand... Can we start all over again?'
				speak_response(text1, 'You')

			if userinput == 'text':
				if not text1:
					text1 = raw_input('You said: ')
					text1 = str(text1)
				else:
					speak_response(text1, 'You')

			if userinput == 'bot':
				if 'text2' in locals():
					try:
						result = API.talk(user_key, app_id, host, botname, text2, session_id=True, recent=True)
					except:
						result = "... I could be all wrong... "
					pb_text1 = result['response']
					botresponse1 = bot.get_response(text2)
					text1 = pb_text1 + ' ' + botresponse1
				speak_response(text1, 'YouBot')

			# Dialog responder to come up with the response to the previous message
			text2 = get_bot_response()
			speak_response(text2, 'Pyggy')

			# Save the back and forth to the CSV log
			newtime = time.time()
			time_elapsed = newtime-timenow
			writer.writerow([newtime,newtime-timenow,text1,text2])
			csvfile.flush()

			text1 = None
