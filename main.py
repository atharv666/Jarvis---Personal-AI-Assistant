# This is Jarvis ai a personal assistant who can chat interactively, write emails in a new file, open specific songs and videos in the computer, open sites and even enter gmail id
import os

import speech_recognition as sr
import win32com.client
import webbrowser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from mutagen.mp3 import MP3
from moviepy.editor import VideoFileClip

import openai
import google.generativeai as genai
import datetime

from config import apikey

import random


speaker = win32com.client.Dispatch("SAPI.spVoice")
#SAPI is speech Application Programming Interface


chatStr =""
def ai(prompt):
    text1 = f"Openai response for Prompt: {prompt} \n**************** \n\n"
    # print(chatStr)
    genai.configure(api_key=apikey)

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [prompt],
            },
        ]
    )
    response = chat_session.send_message(prompt)
    text1 += response.text
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    #     here though i have mentioned openai i have used gemini api

    # with open(f"Openai/prompt- {random.randint(1, 134356455)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split("intelligence")[1:])}.txt", "w") as f:
        f.write(text1)

def chat(query):
    global chatStr
    # print(chatStr)
    genai.configure(api_key=apikey)

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chatStr += f"Atharv:{query}\n"

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [query],
            },
        ]
    )
    response = chat_session.send_message(query)
    speaker.speak(response.text)
    chatStr += f"Jarvis:{response.text}\n"
    return response.text

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        # the above can be changed
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said:{query}")
            return query
        except Exception as e:
            return "Some error occurred. Sorry from Jarvis"


def navigate_to_website(url, email = None, password = None):
    driver = webdriver.Edge()
    driver.get(url)

    if "gmail" in url:
        try:
            time.sleep(2) #wait for the page to load
            email_field = driver.find_element(By.ID, "identifierId")
            email_field.send_keys(email)
            email_field.send_keys(Keys.ENTER)

            time.sleep(2) #wait for the password field to appear
            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys(password)
            password_field.send_keys(Keys.ENTER)
            time.sleep(5) #wait for the login process to complete
        except Exception as e:
            print(f"An error occurred:{e}")


# chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
# webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))

speaker.speak("Welcome Sir I am Jarvis Ai ")
while True:
    print("Listening.....")
    query = takeCommand()
    command_executed = False
    sites = [["wikipedia", "https://wikipedia.com/"], ["youtube", "https://youtube.com/"], ["google", "https://google.com"], ["gmail", "https://gmail.com/"]]
    for site in sites:
        if f"open {site[0]}" in query.lower():
            if site[0] == "gmail":
                speaker.speak(f"logging into {site[0]} sir..")
                navigate_to_website(site[1], "AtharvRaob@gmail.com", "*****")
                command_executed = True
            else:
                speaker.speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                # webbrowser.get("chrome").open(site[1])
                # if "open youtube" in query.lower():
                #     print("Opening Youtube")
                #     webbrowser.open("https://youtube.com/")
                command_executed = True

    if command_executed:
        continue

    songs = [{"name" : "slime song", "path" : "C:/Users/lenovo/Downloads/slime.mp3"},
             {"name" : "nss song", "path" : "C:/Users/lenovo/Downloads/Egzod, Maestro Chives, Neoni - Royalty [NCS Release].mp3"}]
    musicPath = None
    for song in songs:
        if song["name"] in query.lower():
            musicPath = song["path"]
            break
    if musicPath:
        speaker.speak(f"opening {song["name"]} sir..")
        os.startfile(musicPath)
        audio = MP3(musicPath)
        song_length = audio.info.length
        time.sleep(song_length)
        continue

    videos = [["video 1", "C:/Users/lenovo/Desktop/Atharv html/videos/That Time I Got Reincarnated as a Slime - Opening 1 _ 4K _ 60FPS _ Creditless _.mp4"],
              ["video 2", "C:/Users/lenovo/Desktop/Atharv html/videos/That Time I Got Reincarnated as a Slime - Opening 3 _ 4K _ 60FPS _ Creditless _.mp4"],
              ["video 3", "C:/Users/lenovo/Desktop/Atharv html/videos/That Time I Got Reincarnated as a Slime Season 3 - Opening 2 _ Renacer Serenade.mp4"]]
    for video in videos:
        if f"open {video[0]}" in query.lower():
            speaker.speak(f"Opening {video[0]} sir..")
            os.startfile(video[1])
            video = VideoFileClip(video[1])
            video_duration = video.duration
            time.sleep(video_duration)
            command_executed = True

    if command_executed:
        continue

    if "the time" in query.lower():
        # Time = datetime.datetime.now().strftime("%H:%M:%S")
        # speaker.speak(f"Sir the time now is {Time}")
        # the above  can further be customized
        Hour = datetime.datetime.now().strftime("%H")
        Min = datetime.datetime.now().strftime("%M")
        speaker.speak(f"Sir the time now is {Hour} {Min}")
        continue

    if "exit" in query.lower():
        speaker.speak("Goodbye sir...")
        break

    if "reset" in query.lower():
        chatStr = ""
        continue

    if "using artificial intelligence" in query.lower():
        ai(prompt=query)
        continue

    else:
        chat(query)