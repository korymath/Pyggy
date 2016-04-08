from os import system
import warnings
import time
from keys import uk, aid
import speech_recognition as sr
from pb_py import main as API
import csv
import random
from chatterbot import ChatBot
import os.path
import re
import sys
import thread
import random

def speak_who(text, name):
	print name + " said: " + text
	if name == 'YouBot':
		if robotoutput == 'voiceandtext':
			system("say -v Tom -r 180 " + text) 
		return True
	elif name == 'Pyggy':
		if robotoutput == 'voiceandtext':
			system("say -v Samantha -r 180 " + text)
		return True
	else:
		return False

def speak_response(response, name):
	bot_response = response
	
	# Some basic data cleaning
	bot_response = bot_response.replace("<u>", "")
	bot_response = bot_response.replace("</u>", "")
	bot_response = bot_response.replace("\n", "")
	regex = re.compile('[^a-zA-Z0-9 ,.?!]')
	bot_response = regex.sub('', bot_response)
	return speak_who(bot_response, name)

def get_pb_response(seed_text):
	try:
		result = API.talk(user_key, app_id, host, botname, seed_text, session_id=True, recent=True)
		return result['response']
	except:
		result = "... I could be all wrong, but... "
		return result

def get_bot_response(text_input, bot_name):
	pb_text = get_pb_response(text_input)
	botresponse = bot_name.get_response(text_input)

	# Randomly continue down conversation chains
	comb_choice = random.random()
	if comb_choice < 0.7:
		text_output = pb_text + ' ' + botresponse
	elif comb_choice >= 0.7 and comb_choice < 0.85:
		text_output = pb_text
	elif comb_choice >= 0.85:
		text_output = botresponse
	return  text_output

def get_voice_input():
	audio = r.listen(source)
	try:
		input_text = r.recognize_google(audio)
	except:
		input_text = '...something I could not understand... Can we start all over again?'
	return input_text

def get_text_input():
	input_text = raw_input('You said: ')
	return str(input_text)

def write_to_log(newtime, input_text, response_text):
	writer.writerow([newtime,input_text,response_text])
	csvfile.flush()

## Main Program Starts Here

bot_pyggy = ChatBot("Pyggy",
	# read_only=True,
    storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",
    logic_adapters=[
        "chatterbot.adapters.logic.ClosestMatchAdapter"
    ],
    io_adapters=[
        "chatterbot.adapters.io.NoOutputAdapter"
    ],
    database="database_movie_20000_rand_pyggy_new5")

# Only need to train this once
bot_pyggy.train("chatterbot.corpus.english.movielines20000_rand_pyggy")

bot_blue = ChatBot("Blue",
	# read_only=True,
    storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",
    logic_adapters=[
        "chatterbot.adapters.logic.ClosestMatchAdapter"
    ],
    io_adapters=[
        "chatterbot.adapters.io.NoOutputAdapter"
    ],
    database="database_movie_20000_rand_blue_new5")

# Only need to train this once
bot_blue.train("chatterbot.corpus.english.movielines20000_rand_blue")
	
host = 'aiaas.pandorabots.com'
user_key = uk
app_id = aid
botname = 'pyggy2'

# Set some default inputs
if (len(sys.argv) < 2):
	userinput = 'bot' # or 'voice' or 'bot'
else:
	userinput = sys.argv[1]

if (len(sys.argv) < 3):
	robotoutput = 'text' # or 'voiceandtext'
else:
	robotoutput = sys.argv[2]

if (len(sys.argv) < 4):
	if userinput == 'bot':
		input_text = 'Food is human energy.'
	else:
		input_text = None
else:
	input_text = sys.argv[3]

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
				input_text = get_voice_input()
				speak_response(input_text, 'You')

			if userinput == 'text':
				if not input_text:
					input_text = get_text_input()
				else:
					# Handle the first line of dialog nicely
					speak_response(input_text, 'You')	

			if userinput == 'bot':
				if ('response_text' in locals()):
					input_text = get_bot_response(response_text, bot_pyggy)
				
				speak_response(input_text, 'YouBot')

			# Dialog responder to come up with the response to the previous message
			response_text = get_bot_response(input_text, bot_blue)
			speak_response(response_text, 'Pyggy')

			# Save the back and forth to the CSV log
			write_to_log(time.time(),input_text,response_text)

			# Reset the diaglog text
			input_text = None
