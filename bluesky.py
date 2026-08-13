from atproto import Client
from dataclasses import dataclass
from datetime import datetime, timezone
from flask import session
import json
import os
from PIL import Image
import requests
import urllib.request

pds_url = "moonphasebot.bsky.social"
IMAGE_MIMETYPE = "image/jpg"

# Moon Phases
GIBBOUS = "Gibbous"
CRESCENT = "Crescent"
FULL_MOON = "Full Moon"
NEW_MOON = "New Moon"
HALF_MOON = "Half Moon"

WAXING = "Waxing"
WANING = "Waning"

# API Keywords
AGE = "age"
PHASE = "phase"
IMAGE = "image"
URL = "url"



class Moon:
    age: float
    phasePercentage: float
    imageUrl: str
    lastMajorPhase : str
    
    def __init__(self, age, phasePercentage, imageUrl, lastMajorPhase):
        self.age = age
        self.phasePercentage = phasePercentage
        self.imageUrl = imageUrl
        self.lastMajorPhase = lastMajorPhase
    
    def saveToFile(data):
        with open("phase.json", "w") as file:
            json.dump(data, file)
            file.close()

    def waxWane(self): 
        if (self.lastMajorPhase == NEW_MOON and self.phasePercentage < 99 and self.phasePercentage > 1):
            return WAXING
        elif (self.lastMajorPhase == FULL_MOON and self.phasePercentage < 99 and self.phasePercentage > 1):
            return WANING
        else: 
            return ""

    def moonType(self):
        if (self.phasePercentage > 51 and self.phasePercentage < 99):
            return GIBBOUS
        elif (self.phasePercentage < 49 and self.phasePercentage > 1):
            return CRESCENT
        elif (self.phasePercentage > 99):
            return FULL_MOON
        elif (self.phasePercentage < 1): 
            return NEW_MOON
        else: 
            return HALF_MOON



# Used to track waxing vs. waning as this is not available/easily parsed from NASA dataset

def getLastMajorPhase(phasePercentage: float):
    lastMajorPhase = ""

    if phasePercentage > 99:
        lastMajorPhase = FULL_MOON
        data = {
            "lastMajorPhase" : FULL_MOON
        }
        saveToFile(data)
    elif phasePercentage < 1:
        lastMajorPhase = NEW_MOON
        data = {
            "lastMajorPhase" : NEW_MOON
        }
    else:
        with open("phase.json", "r") as f:
            data = json.load(f)
            lastMajorPhase = data["lastMajorPhase"]
            f.close()

    return lastMajorPhase


def getMoonInfo():
    date = datetime.now().strftime('%Y-%m-%d'+'T%H:%M')
    data = requests.get(f"https://svs.gsfc.nasa.gov/api/dialamoon/{date}")
    moonData = data.json()
    lastMajorPhase = getLastMajorPhase(moonData[PHASE])
    
    moon = Moon(moonData[AGE], moonData[PHASE], moonData[IMAGE][URL], lastMajorPhase)

    return moon


def main():
    
    client = Client()
    password = os.getenv("BSKY_KEY")
    client.login(pds_url, password)
    moon = getMoonInfo()

    wax_wane = moon.waxWane()
    moon_type = moon.moonType()

    image = urllib.request.urlretrieve(moon.imageUrl, "moon.jpg")
    with open('moon.jpg', 'rb') as f:
        img_data = f.read()

    post_text = "Phase: {} {} \nVisible Percentage: {} \nAge: {}".format(wax_wane, moon_type, moon.phasePercentage, moon.age)    

    alt_text = "{} {} at {}%".format(wax_wane, moon_type, moon.phasePercentage)

    try:
        client.send_image(text=post_text, image=img_data, image_alt=alt_text)
        print("Post sent successfully")
    except Exception as e:
        print(f"Error has occursed with poasting. Please fix. Detailed as {e}")


main()
