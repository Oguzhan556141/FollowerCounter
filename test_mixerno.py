import requests
import json
headers = {"User-Agent": "Mozilla/5.0"}
try:
    r = requests.get("https://mixerno.space/api/instagram-user/gulftechtr", headers=headers)
    print("mixerno:", r.status_code, r.text[:200])
except Exception as e:
    print(e)
try:
    r = requests.get("https://counts.live/api/instagram-follower-count/gulftechtr/data")
    print("counts.live:", r.status_code, r.text[:200])
except Exception as e:
    pass
