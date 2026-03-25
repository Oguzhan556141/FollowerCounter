import requests
import re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def test_instagram():
    url = "https://www.instagram.com/gulftechtr/"
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print("IG status:", r.status_code)
        if "login" in r.url:
            print("Redirected to login")
        m = re.search(r'content="(\d+[.,\d]*)\s*Followers', r.text, re.IGNORECASE)
        print("IG meta match:", m.group(1) if m else "None")
    except Exception as e:
        print("IG error:", e)

def test_picuki():
    url = "https://www.picuki.com/profile/gulftechtr"
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print("Picuki status:", r.status_code)
        # Look for Followers keyword
        m2 = re.search(r'>Followers<.*?>([\d,.]+)<', r.text, re.IGNORECASE | re.DOTALL)
        print("Picuki match:", m2.group(1).strip() if m2 else "None")
    except Exception as e:
         print("Picuki error:", e)
         
def test_greatfon():
    url = "https://greatfon.com/v/gulftechtr"
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print("Greatfon status:", r.status_code)
        if "Followers" in r.text:
            m = re.search(r'Followers.*?<span[^>]*>([\d,.]+)</span>', r.text, flags=re.IGNORECASE | re.DOTALL)
            print("Greatfon match:", m.group(1).strip() if m else "None")
    except Exception as e:
        print("Greatfon error:", e)

if __name__ == '__main__':
    test_instagram()
    test_picuki()
    test_greatfon()
