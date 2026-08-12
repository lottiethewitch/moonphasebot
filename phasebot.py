from atproto import Client
from dataclasses import dataclass
from datetime import datetime
import json
import os
from PIL import Image
import requests
import urllib.request

class Moon:
    age: float
    phasePercentage: float
    imageUrl: str
    lastMajorPhase : str
    
    
    def __init__(age, phasePercentage, imageUrl):
        self.age = age
        self.phasePercentage = phasePercentage
        self.imageUrl = imageUrl
        self.lastMajorPhase = getLastMajorPhase()
    
    def saveToFile(data):
        with open("phase.json", "w") as file:
            json.dump(data, file)
            file.close()

    def waxWane(): 
        if (lastMajorPhase == "NEW" and phasePercentage < 99 and phasePercentage > 1):
            return "Waxing"
        elif (lastMajorPhase == "FULL" and phasePercentage < 99 and phasePercentage > 1):
            return "Waning"

    def moonType():
        if (self.phasePercentage > 51 and self.phasePercentage < 99):
            return "Gibbous"
        elif (self.phasePercentage < 49 and self.phasePercentage > 1):
            return "Crescent"
        elif (phasePercentage > 99):
            return "Full Moon"
        elif (phasePercentage < 1): 
            return "New Moon"
        else: 
            return "Half Moon"

    # Used to track waxing vs. waning as this is not available/easily parsed from NASA dataset
    def getLastMajorPhase():
        if self.phasePercentage > 99:
            self.lastMajorPhase = "FULL"
            data = {
                "lastMajorPhase" : "FULL"
            }
            saveToFile(data)
        elif self.phasePercentage < 1:
            self.lastMajorPhase = "NEW"
            data = {
                "lastMajorPhase" : "NEW"
            }
        else:
            with open("phase.json", "r") as f:
                data = json.load(f)
                self.lastMajorPhase = data["lastMajorPhase"]
                f.close()


def getClient():
    client = Client()
    password = os.getenv("BSKY_KEY")
    client.login('moonphasebot.bsky.social', password)
    return client


def makePost(moon: Moon, client: Client):

    image = urllib.request.urlretrieve(moon.imageUrl, "moon.jpg")
    with Image.open(r"moon.jpg") as im:
        img_bytes = im.read()
        width, height = im.size
    # this size limit is specified in the app.bsky.embed.images lexicon
    if len(img_bytes) > 2000000:
        raise Exception(
            f"image file size too large. 2000000 bytes maximum, got: {len(img_bytes)}"
        )

    resp = requests.post(
        pds_url + "/xrpc/com.atproto.repo.uploadBlob",
        headers={
            "Content-Type": IMAGE_MIMETYPE,
            "Authorization": "Bearer " + session["accessJwt"],
        },
        data=img_bytes,
    )
    resp.raise_for_status()
    blob = resp.json()["blob"]

    post["embed"] = {
        "$type": "app.bsky.feed.post",
        "text": f"{moon.waxWane} {moon.moonType} \n phase percentage: {moon.phasePercentage} \n age: {moon.age}",
        "createdAt": now,
        "images": [{
            "alt": f"{moon.waxWane} {moon.moonType} as of right now",
            "image": blob,
            "aspectRatio": {
                "width": width,
                "height": height
            }
        }]
    }

    return post


def getMoonInfo():
    date = datetime.now().strftime('%Y-%m-%d'+'T%H:%M')
    data = requests.get(f"https://svs.gsfc.nasa.gov/api/dialamoon/{date}")
    moonData = data.json() 
    
    moon = Moon()
    moon.__init__(
        age = moonData["age"],
        phasePercentage = moonData["phasePercentage"],
        imageUrl = moonData["image.url"],
    )

    return moon


def main():
    client = getClient()
    moon = getMoonInfo()
    client.post(makePost(moon))

