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

bot = ChatBot("Terminal",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapters=[
        "chatterbot.adapters.logic.EvaluateMathematically",
        "chatterbot.adapters.logic.TimeLogicAdapter",
        "chatterbot.adapters.logic.ClosestMeaningAdapter"
    ],
    io_adapters=[
        "chatterbot.adapters.io.NoOutputAdapter"
    ],
    database="database-big.db")

# check if the database file exists
# if not, then train it
bot.train("chatterbot.corpus.english.movielines")
	
host = 'aiaas.pandorabots.com'
user_key = uk
app_id = aid
botname = 'pyggy2'

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
# 
def speak_who(text, name):
	print(name + " said: " + text)
	if name == 'Fiona':
		system("say -v Tom -r 200 " + text) # should be Tom
	else:
		system("say -v Samantha -r 200 " + text) # should be Samantha

def speak_response(response, name):
	bot_response = response
	# Some basic data cleaning
	bot_response = bot_response.replace("'", "")
	bot_response = bot_response.replace("\n", "")
	bot_response = bot_response.replace("(", "")
	bot_response = bot_response.replace(")", "")
	bot_response = bot_response.replace(";", "")
	speak_who(bot_response, name)

# obtain audio from the microphone	
# warnings.filterwarnings("ignore")
# r = sr.Recognizer()

timenow = time.time()
with open('logs/' + str(timenow) + '_log.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile)
		fieldnames = ['timestamp', 'input_text', 'response']
		writer.writerow(fieldnames)
		text1 = "Good Morning"
		# text1 = "What is your name?"
		
		while True:
			# Fiona says something (chatterbot)
			speak_response(text1, 'Fiona')

			# Pyggy responds (pandorabot)
			result = API.talk(user_key, app_id, host, botname, text1, session_id=True, recent=True)
			text2 = result['response']
			
			# time.sleep(0.1)
			speak_response(text2, 'Rosie')

			# Save the back and forth to the CSV log
			writer.writerow([time.time(),text1,text2])
			csvfile.flush()

			# Fiona updates what to say next (random choice of bot seed)
			coin = random.random()
			highLim = 0.99
			lowLim = 0.01

			if coin > highLim:
				result = API.talk(user_key, app_id, host, botname, text1, session_id=True, recent=True)
				text1 = result['response']
			elif coin < highLim and coin > lowLim:
				text1 = bot.get_response(text2)	
			else:
				text1 = ngram.generate_text(lm, 8, nletters=100)

			# time.sleep(0.1)




