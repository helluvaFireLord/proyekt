import speech_recognition as speech_recog
from random import choice, randint
import time




def speach():
    mic = speech_recog.Microphone()
    recog = speech_recog.Recognizer()

    with mic as audio_file:
        print("talk about smtng")
        recog.adjust_for_ambient_noise(audio_file)
        audio = recog.listen(audio_file)
        return recog.recognize_google(audio, language="ru-RU")

    




























