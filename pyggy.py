from os import system
import warnings

from keys import uk, aid

import speech_recognition as sr
from pb_py import main as API

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

opener = "Why don't you start the conversation?"
speak_response(opener)

# obtain audio from the microphone	
warnings.filterwarnings("ignore")
r = sr.Recognizer()
with sr.Microphone() as source:
	while True:
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
		input_text = r.recognize_google(audio)
		print("You said: " + input_text)
		result = API.talk(user_key, app_id, host, botname, input_text, session_id=True, recent=True)
		speak_response(result['response'])





