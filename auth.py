# auth.py
import os, time, requests
from dotenv import load_dotenv
load_dotenv()


TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

_token = None
_exp = 0

def get_app_token() -> str:
    global _token, _exp
    now = time.time()
    if _token and now < _exp:
        return _token
    r = requests.post(TWITCH_TOKEN_URL, 
                      data={
                            "client_id": CLIENT_ID,
                            "client_secret": CLIENT_SECRET,
                            "grant_type": "client_credentials"
                        }, 
                        timeout=20)
    r.raise_for_status()
    data = r.json()
    _token = data["access_token"]
    _exp = now + data.get("expires_in", 0) - 60
    return _token
