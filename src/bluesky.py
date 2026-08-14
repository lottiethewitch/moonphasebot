from atproto import Client
import json
import os
from PIL import Image
import requests

# local 
import moon
from moon import getMoonInfo

pds_url = "moonphasebot.bsky.social"

def main():
    
    client = Client()
    password = os.getenv("BSKY_KEY")
    client.login(pds_url, password)
    moon = getMoonInfo()

    wax_wane = moon.waxWane()
    moon_type = moon.moonType()

 
    with open('../moon.jpg', 'rb') as f:
        img_data = f.read()

    post_text = "Phase: {} {} \nVisible Percentage: {} \nAge: {}".format(wax_wane, moon_type, moon.phasePercentage, moon.age)    

    alt_text = "{} {} at {}%".format(wax_wane, moon_type, moon.phasePercentage)

    
    try:
        client.send_image(text=post_text, image=img_data, image_alt=alt_text)
        print("Post sent successfully")
    except Exception as e:
        print(f"Error has occursed with poasting. Please fix. Detailed as {e}")


main()
