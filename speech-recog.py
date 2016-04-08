#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import time

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:

    while True:
        print("Say something!")
        audio = r.listen(source)

        # recognize speech using Sphinx
        try:
            s_s = time.time()
            print 'Sphinx start: ' + str(s_s)
            print("Sphinx thinks you said " + r.recognize_sphinx(audio))
            s_e = time.time()
            print 'Sphinx end: ' + str(s_e)
            print 'Elapsed Time: ' + str(s_e - s_s)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            g_s = time.time()
            print 'Sphinx start: ' + str(g_s)
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
            g_e = time.time()
            print 'Sphinx end: ' + str(g_e)
            print 'Elapsed Time: ' + str(g_e - g_s)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
