import pyttsx3
import time
import speech_recognition as sr
from random import choice
from utils import opening_text
from datetime import datetime
from decouple import config

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

eng = pyttsx3.init('sapi5')

# Set Rate
eng.setProperty('rate', 160)

# Set Volume
eng.setProperty('volume', 1.0)

# Set Voice
voices = eng.getProperty('voices')
eng.setProperty('voice', voices[1].id)


def main():
    global out

    def sleep():
        time.sleep(0.6)

    def speak(say_this):
        eng.say(say_this)
        eng.runAndWait()

    # Greet the user depending on the local time
    def greet():
        hour = datetime.now().hour
        if (hour >= 0) and (hour < 12):
            print(f"\nGood Morning, {USERNAME}!")
            sleep()
            speak(f"Good Morning {USERNAME}")
        elif (hour >= 12) and (hour < 17):
            print(f"\nGood Afternoon, {USERNAME}!")
            sleep()
            speak(f"Good afternoon {USERNAME}")
        elif (hour >= 17) and (hour < 24):
            print(f"\nGood Evening, {USERNAME}!")
            sleep()
            speak(f"Good Evening {USERNAME}")
        # speak(f"I am {BOTNAME}. What do you want me to say?")

    # sds
    def first_func():
        speak("What do you want me to do?")
        choose_func = input("What do you want me to do?\n")

        while True:
            if choose_func == "Speak" or choose_func == "speak" or choose_func == "SPEAK":
                take_user_input()
            elif choose_func == "Atlas" or choose_func == "atlas" or choose_func == "ATLAS":
                atlas_speak()
            else:
                print("\nInput invalid. Please try again.\n")
                sleep()
                speak("Invalid Input. Please try again")
                continue

    # take user voice input
    def take_user_input():
        """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening....')
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            if not 'exit' in query or 'stop' in query:
                speak(choice(opening_text))
                if 'atlas' in query:
                    atlas_speak()
            else:
                hour = datetime.now().hour
                if 23 >= hour > 18:
                    speak(f"Good night {USERNAME}, take care!")
                else:
                    speak(f'Have a good day {USERNAME}!')
                exit()
        except Exception:
            speak('Sorry, I could not understand. Could you please say that again?')
            query = 'None'
        return query

    # let atlas speak
    def atlas_speak():
        # ask the user what to say
        while True:
            speak(input("What do you want atlas to say: \n"))

            # Check if user wants atlas to speak again
            while True:
                inp = input("Do you want Atlas to speak again: \n")
                print(" ")
                if inp == "No" or inp == "no" or inp == "NO":
                    print("Bye! I hope to see you again.")
                    sleep()
                    speak(f"Goodbye {USERNAME}! I hope to see you again")
                    out = 0
                    break
                elif inp == "Yes" or inp == "yes" or inp == "YES":
                    out = 1
                    break
                else:
                    sleep()
                    speak("That input is invalid, please try again.")
                    continue

            # 0 = user wants to stop, 1 = user wants to try another
            if out == 0:
                first_func()
                break
            elif out == 1:
                continue

    # Ths is where everything starts
    greet()
    first_func()



main()

