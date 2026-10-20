from playsound import playsound
import pywhatkit as kit
import eel
import os
import sqlite3
import webbrowser
import re
from engine.command import speak
from engine.config import ASSISTANT_NAME


conn = sqlite3.connect("sophia.db")

cursor = conn.cursor()

#sound function for playing sound
def playAssistantSound():
    music_dir = "C:\\Users\\shahi\\OneDrive\\Desktop\\sophia\\www\\assets\\www_assets_audio_start_sound.mp3"
    playsound(music_dir)

#click sound for mic button

@eel.expose
def playClickSound():
    music_dir = "C:\\Users\\shahi\\OneDrive\\Desktop\\sophia\\www\\assets\\www_assets_audio_click_sound (1).mp3"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "").strip().lower()

    if query != "":
        try:
            # Try to find the application in sys_command table
            cursor.execute('SELECT path FROM sys_command WHERE LOWER(name) = ?', (query,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])
                return

            # If not found, try to find the URL in web_command table
            cursor.execute('SELECT url FROM web_command WHERE LOWER(name) = ?', (query,))
            results = cursor.fetchall()
            
            if len(results) != 0:
                speak("Opening " + query)
                webbrowser.open(results[0][0])
                return

            # If still not found, try to open using os.system
            speak("Opening " + query)
            try:
                os.system('start ' + query)
            except Exception as e:
                speak(f"Unable to open {query}. Error: {str(e)}")

        except Exception as e:
            speak(f"Something went wrong: {str(e)}")
