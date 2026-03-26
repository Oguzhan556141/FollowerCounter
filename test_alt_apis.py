import requests
import json
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

def check(url):
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"URL: {url}")
        print(f"Status: {r.status_code}")
        print(f"Text: {r.text[:200]}\n")
    except Exception as e:
        print(f"Failed {url}: {e}\n")

check("https://mixerno.space/api/instagram-user/gulftechtr")
check("https://counts.live/api/instagram-follower-count/gulftechtr/data")
check("https://tokcount.com/api/v1/instagram/user/gulftechtr")
check("https://api.statscrop.com/api/v1/social/instagram/gulftechtr")
