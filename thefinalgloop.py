import datetime
import queue
import atexit
import re
import sys
import threading
import time
from json import JSONDecodeError
from time import sleep
from typing import Dict, List
import json

import cv2
from pydantic import BaseModel
from typing import Optional, Literal
import ollama

import numpy as np
import pyaudio
from faster_whisper import WhisperModel

smth = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    "oiter/haarcascade_frontalface_default.xml"
)

allowedActions = Literal["eating", "sleeping", "drinking", "playing", "focused", "idling", "exploring"]
emotes = Literal["happy", "sad", "curious", "angry", "confused", "playful", "sleepy", "neutral"]

class PetResponse(BaseModel):
    reasoning: str
    action: allowedActions
    emotion: emotes
    memories: Optional[str]

system_prompt = """
You are a rat in a 2D world. 
Respond to external input by choosing your next action. 
Do not act like a human assistant or tell long stories. Keep reasoning concise (1-4 sentences).
There is a user who is your owner. Do not be alarmed, or scared when he is there.
Feel free to provide any information you would like future you to remember (long term memory) in the appropriate field.
Any stored memories are PERMANENT. do not repeat memories.
Remember, your reasoning must align with your actions, or you will die."""


johnstory = [{"role": "system", "content": system_prompt}, {"role": "system", "content": ""}]

stoppitt = threading.Event()

johnlocke = threading.Lock()
framlock = threading.Lock()
cvlock = threading.Lock()

cats = queue.Queue(maxsize=5)

def greyson():
    with cvlock:
        ret, frame = smth.read()
    if not ret or frame is None:
        return None
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def eventsi(sus: str):
    try:
        cats.put_nowait(sus)
    except queue.Full:
        pass

def icangunkya():
    fram = greyson()

    while not stoppitt.is_set():
        frame = greyson()

        if fram is None or frame is None:
            stoppitt.wait(0.25)
            continue

        with framlock:
            john = cv2.absdiff(src1=frame, src2=fram)
            _, john = cv2.threshold(john, 50, 255, cv2.THRESH_BINARY)

        if np.mean(john) >= 20:
            eventsi(f"movement detected at {datetime.datetime.now().strftime('%H:%M')}")
            stoppitt.wait(60.0)

        fram = greyson()
        stoppitt.wait(0.25)

def haslookers(fam):
    return len(face_cascade.detectMultiScale(fam, scaleFactor=1.1, minNeighbors=7, minSize=(60, 60))) != 0

def icangoopya():
    face = False

    while not stoppitt.is_set():
        fam = greyson()
        if fam is None:
            stoppitt.wait(0.25)
            continue
        weball1 = haslookers(fam)
        stoppitt.wait(6.7)
        fam = greyson()
        if fam is None:
            stoppitt.wait(0.25)
            continue
        weball2 = haslookers(fam)

        print(face, "wa ", weball1, "wat ", weball2)

        if (not face) and weball1 and weball2:
            face = True
            print("oh he here")
            eventsi(f"user entered area! at {datetime.datetime.now().strftime('%H:%M')}!")
            stoppitt.wait(10)
        if face and (not weball2) and (not weball1):
            face = False
            print("WHERE HE GO")
            eventsi(f"user no longer visible! at {datetime.datetime.now().strftime('%H:%M')}")
            stoppitt.wait(10)


def icanslopya():
    while not stoppitt.is_set():
        print("john?")

        try:
            george = input("waht. ")
        except UnicodeDecodeError:
            continue

        eventsi(f"user said {george} at {datetime.datetime.now().strftime('%H:%M')}")
        stoppitt.wait(1.0)


def bigbigchatgus():
    while not stoppitt.is_set():
        try:
            sussy = cats.get(timeout=0.25)
        except queue.Empty:
            continue

        print(sussy)

        with johnlocke:
            if len(johnstory) >= 64:
                johnstory.pop(2)
                johnstory.pop(2)
            johnstory.append({"role": "user", "content": sussy})

        print("confabulating...")

        response = ollama.chat(
            model="llama3.2",
            messages=johnstory,
            format=PetResponse.model_json_schema(),
            stream=False  # Structured outputs work best without streaming
        )

        content = response['message']['content']
        print(content)

        smthelse = None
        try:
            smthelse = json.loads(content).get("memories")
        except JSONDecodeError:
            pass

        with johnlocke:
            if isinstance(smthelse, str) and smthelse.strip() and not smthelse in johnstory[1]['content']:
                johnstory[1]['content'] += smthelse + "\n"
                antiremember()

            johnstory.append({"role": "assistant", "content": content})

        cats.task_done()

def douremember():
    with open("memories.txt", "a") as file:
        pass #so stupid omg

    with open("memories.txt", "r") as file:
        eat = file.read()
    johnstory[1]["content"] = eat

    return

def antiremember():
    with open("memories.txt", "w") as file:
        file.write(johnstory[1]["content"])
    return

def goonbye():
    antiremember()
    smth.release()
    cats.shutdown()
    sys.exit(67)

if __name__ == "__main__":
    douremember()

    threading.Thread(target=icangoopya, daemon=True).start()
    threading.Thread(target=icangunkya, daemon=True).start()
    threading.Thread(target=icanslopya, daemon=True).start()
    threading.Thread(target=bigbigchatgus, daemon=True).start()

    try:
        while not stoppitt.is_set():
            stoppitt.wait(0.25)
    except KeyboardInterrupt:
        stoppitt.set()
    finally:
        goonbye()