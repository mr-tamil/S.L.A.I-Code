import os
import database  # Created by our team
from pydub import AudioSegment
from pydub.playback import play
from pyttsx3 import engine
import pyttsx3


# get the list of voice ids from the system
def getVoiceids():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_list_info  = {}
    for voice in voices:
        # to get the info. about various voices in our PC
        voice_data = {voice.name: {"ID": voice.id,
                                   "Age": voice.age,
                                   "Gender": voice.gender,
                                   "Languages Known":voice.languages}}

        voice_list_info.update(voice_data)

    return voice_list_info


# Speak the inserted text
def SpeakText(text):
    # get property data from database
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
    db = database.Database(db_path)
    data = db.table_data("system")
    speed_rate, volume, voice, *others = [i[2] for i in data]
    # create engine
    engine = pyttsx3.init()
    try:
        engine.setProperty('rate', int(speed_rate))  # Default to 140
        engine.setProperty('volume', volume/100)  # Default to 0.5
        if voice == "female":  # default to male
            id = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0'
        engine.setProperty("voice", id)

    except Exception as e:
        print(e)

    engine.say(text)
    engine.runAndWait()


# if __name__ == "__main__":
#     text = "Hello Sindhu and BTS Jung Kook!, I am the Personal assistant to you. If you asks me to do some thing, I can able to do."
#     SpeakText(text)
    # print(getVoiceids())


# print(getVoiceids())

# for playing wav file
# song = AudioSegment.from_wav("recording1.wav")


# for playing mp3 file
# song = AudioSegment.from_mp3("recording1.mp3")
# play(song)
