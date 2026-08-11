from atproto import Client
import os

client = Client()
password = os.getenv("BSKY_KEY")
client.login('moonphasebot.bsky.social', password)


