import json
import requests
from datetime import datetime, timezone

from utils import saveImage

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
    json_file: str
    
    def __init__(self, age, phasePercentage, imageUrl, json_file):
        self.age = age
        self.phasePercentage = phasePercentage
        self.imageUrl = imageUrl
        self.json_file = json_file
    
    def saveToFile(data):
        with open(JSON_FILE, "w") as file:
            json.dump(data, file)
            file.close()

    def waxWane(self):
        lastMajorPhase = self.getLastMajorPhase()
        if (lastMajorPhase == NEW_MOON and self.phasePercentage < 99 and self.phasePercentage > 1):
            return WAXING
        elif (lastMajorPhase == FULL_MOON and self.phasePercentage < 99 and self.phasePercentage > 1):
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


    def getLastMajorPhase(self):
        lastMajorPhase = ""

        if self.phasePercentage > 99:
            lastMajorPhase = FULL_MOON
            data = {
                "lastMajorPhase" : FULL_MOON
            }
            saveToFile(data)
        elif self.phasePercentage < 1:
            lastMajorPhase = NEW_MOON
            data = {
                "lastMajorPhase" : NEW_MOON
            }
        else:
            with open(JSON_FILE, "r") as f:
                data = json.load(f)
                lastMajorPhase = data["lastMajorPhase"]
                f.close()
        return lastMajorPhase


# API

def getMoonInfo(json_file):
    date = datetime.now().strftime('%Y-%m-%d'+'T%H:%M')
    data = requests.get(f"https://svs.gsfc.nasa.gov/api/dialamoon/{date}")
    moonData = data.json()
    
    moon = Moon(moonData[AGE], moonData[PHASE], moonData[IMAGE][URL], json_file)
    saveImage(moon.imageUrl, "../moon.jpg")

    return moon




