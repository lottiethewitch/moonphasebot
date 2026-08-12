import json
import phasebot
import requests
import unittest
import phasebot
from datetime import datetime

date = datetime.now().strftime('%Y-%m-%d'+'T%H:%M')
data = requests.get(f"https://svs.gsfc.nasa.gov/api/dialamoon/{date}")
moonData = data.json()

print(moonData["phase"])

client = phasebot.getClient()
moon = getMoonInfo()
post = makePost(moon, client)
print(post)
