from atproto import Client
from dataclasses import dataclass
from datetime import datetime, timezone
from flask import session
import json
import os
from PIL import Image
import requests
import urllib.request

import moon

pds_url = "moonphasebot.bsky.social"
IMAGE_MIMETYPE = "image/jpg"


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
