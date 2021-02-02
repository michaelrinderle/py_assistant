# scom  
# python3 -m vemv env
# env/Scripts/activate

# pip install speechrecognition playsound gtts 
# pip install .\PyAudio-0.2.11-cp38-cp38-win_amd64.whl

# pypy -m pip install pipwin

import speech_recognition as speech
import subprocess
import playsound
import os 
import uuid
from gtts import gTTS
import webbrowser

recognizer = speech.Recognizer()

def speak(audio_data):
    tts = gTTS(text=audio_data, lang='en')
    audio_mp3 = str(uuid.uuid4()) + ".mp3"
    tts.save(audio_mp3)
    playsound.playsound(audio_mp3)
    os.remove(audio_mp3)

def record():
    with speech.Microphone() as mic_source:
        audio = recognizer.listen(mic_source, timeout=3, phrase_time_limit=3)
        voice_data = ''
        try:
            voice_data = recognizer.recognize_google(audio)
        except speech.UnknownValueError:
            print("no value")
        except speech.RequestError:
            print("error")
        print(voice_data)
        return voice_data.lower()

def response(voice_data):
    print(voice_data)
    if contains(["shell", "powershell"], voice_data):
        subprocess.Popen(["powershell.exe"], creationflags=subprocess.CREATE_NEW_CONSOLE)

    elif contains(["search", "google"], voice_data):
        speak("search what?")
        search = record()
        url = "https://google.com/search?q=" + search
        webbrowser.get().open(url)

    elif contains(['youtube', "tube"], voice_data):
        speak("search what?")
        search = record()
        if search != "":
            url = "https://youtube.com/results?search_query=" + search
            webbrowser.get().open(url)

    elif contains(["suspend", "hibernate"], voice_data):
        speak("are you sure?")
        shutdown = record().lower()
        if shutdown != "no":
            os.system("shutdown.exe /h")

    else:
        speak("command not recognized")

def contains(terms, voice_data):
    for term in terms:
        if term in voice_data:
            return True

while(1):
    voice_data = record()
    if voice_data != "":
        response(voice_data)