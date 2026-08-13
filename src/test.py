import json
import requests
import unittest
from datetime import datetime



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

#sue me i tested this manually

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



moon = getMoonInfo()
print(moon.moonType())
print(getLastMajorPhase(moon.phasePercentage))
