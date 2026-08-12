import json
import phasebot
import requests
import unittest
from datetime import datetime


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
        if (lastMajorPhase == NEW_MOON and phasePercentage < 99 and phasePercentage > 1):
            return WAXING
        elif (lastMajorPhase == FULL_MOON and phasePercentage < 99 and phasePercentage > 1):
            return WANING

    def moonType(self):
        if (self.phasePercentage > 51 and self.phasePercentage < 99):
            return GIBBOUS
        elif (self.phasePercentage < 49 and self.phasePercentage > 1):
            return CRESCENT
        elif (phasePercentage > 99):
            return FULL_MOON
        elif (phasePercentage < 1): 
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
print(moon.waxWane)
