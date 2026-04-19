import requests
from config import API_KEY, API_SECRET, REDIRECT_URI

def get_login_url():
    return f"https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={API_KEY}&redirect_uri={REDIRECT_URI}"

def generate_access_token(code):

    url = "https://api.upstox.com/v2/login/authorization/token"

    data = {
        "code": code,
        "client_id": API_KEY,
        "client_secret": API_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    res = requests.post(url, headers=headers, data=data)

    if res.status_code != 200:
        return None, res.text

    token = res.json().get("access_token")

    return token, None
