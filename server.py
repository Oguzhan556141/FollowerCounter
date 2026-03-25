import requests
import re
import time
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# Cache for follower count
cache = {
    'count': 816, # Last known verified count as fallback
    'last_updated': int(time.time())
}

def get_instagram_followers(username):
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "x-ig-app-id": "936619743392459",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return int(data['data']['user']['edge_followed_by']['count'])
        else:
            print(f"Instagram request failed. Status code: {response.status_code}")
        return None
    except Exception as e:
        print(f"Error fetching Instagram data: {e}")
        return None

@app.route('/api/followers')
def followers():
    username = 'gulftechtr'
    current_time = int(time.time())
    
    # Update cache if it's older than 30 seconds
    if current_time - cache['last_updated'] > 25: # 25s buffer for 30s logic
        new_count = get_instagram_followers(username)
        if new_count is not None:
            cache['count'] = new_count
            cache['last_updated'] = current_time
            print(f"Updated followers for {username}: {new_count}")
            
    return jsonify({
        'username': username,
        'count': cache['count'],
        'last_updated': cache['last_updated']
    })

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    # Default to 0 if we can't fetch on start
    initial_count = get_instagram_followers('gulftechtr')
    if initial_count:
        cache['count'] = initial_count
        cache['last_updated'] = int(time.time())
    
    print("Starting Gulf Tech Follower Counter Server on http://localhost:5003")
    app.run(host='0.0.0.0', port=5003, debug=True)
