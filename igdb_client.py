import os
from igdb.wrapper import IGDBWrapper
from auth import get_app_token

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")

def wrapper():
    request = IGDBWrapper(CLIENT_ID, get_app_token())
    return request