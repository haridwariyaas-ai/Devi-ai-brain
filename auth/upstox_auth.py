# auth/upstox_auth.py

import requests
from config import API_KEY, API_SECRET, REDIRECT_URI

def get_login_url():
    return f"https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={API_KEY}&redirect_uri={REDIRECT_URI}"

def generate_access_token(code):

    url = "https://api.upstox.com/v2/login/authorization/token"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "code": code,
        "client_id": API_KEY,
        "client_secret": API_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    response = requests.post(url, headers=headers, data=data)

    print("TOKEN RESPONSE:", response.text)

    if response.status_code != 200:
        return None, response.text

    json_data = response.json()

    access_token = json_data.get("access_token")

    if not access_token:
        return None, "Access token missing in response"

    return access_token, None
