import speech_recognition as sr
import os
r = sr.Recognizer()
words = [
    "Fuck",
    "Shit",
    "Crap",
    "Crud",
    "Bitch",
    "Whore",
    "Slut",
    "Faggot",
    "Fag",
    "Kill",
    "Retard",
    "God",
    "Gosh",
    "Damn",
    "Dang",
    "Darn",
    "Dick",
    "Ass",
    "Hell",
    "Heck",
    "Frick",
    "Wanker",
    "Twink",
    "Chud",
    "Jesus",
    "Hate",
    "Flip",
    "Stupid",
    "Midget",
    "Fatass",
    "Tranny"
]
while True:
    try:
        with sr.Microphone(device_index=4) as source:
            print("Listening...")
            
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            text = text.lower()  
            print("You said:", text)
            
            if "exit" in text:
                print("Exiting program...")
                break
            for i in [word.lower() for word in words]:
                if i in text:
                    os.system("pkill chrome")
    except sr.UnknownValueError:
        print("Could not understand audio")

    except KeyboardInterrupt:
        print("Program terminated by user")
        break