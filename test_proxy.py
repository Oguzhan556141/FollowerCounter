import requests
import re
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def test_site(url, regex):
    try:
        r = requests.get(url, headers=headers, timeout=5)
        m = re.search(regex, r.text, flags=re.IGNORECASE|re.DOTALL)
        print(f"{url} -> Status: {r.status_code}, Match: {m.group(1).strip() if m else 'None'}")
    except Exception as e:
        print(f"{url} -> Error: {e}")

test_site("https://greatfon.com/v/gulftechtr", r'>Followers<.*?([\d,]+)')
test_site("https://www.picuki.com/profile/gulftechtr", r'Followers[^>]*>\s*([\d,.]+)</span>')
test_site("https://dumpoir.com/v/gulftechtr", r'Followers[^>]*>\s*([\d,.]+)</span>')
test_site("https://iganony.io/profile/gulftechtr", r'followers.*?([\d,]+)')
test_site("https://imginn.com/gulftechtr/", r'<span class="num">([\d,.]+)</span>.*?[Ff]ollowers')
test_site("https://i.instagram.com/api/v1/users/web_profile_info/?username=gulftechtr", r'"count":(\d+)')

