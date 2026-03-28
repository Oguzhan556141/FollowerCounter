import eventlet
eventlet.monkey_patch()
import requests
import re
import time
import os
import threading
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder='.')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- CONFIGURATION ---
# To avoid 401/429 errors, paste your Instagram 'sessionid' cookie value here:
SESSIONID = '49647639774%3AH966aEpJiF3K48%3A7%3AAYjfwGpXu8Y7kZq9AxCTNcCV2vyag7eiCsoI4pUcjBU' 
USERNAME = 'gulftechtr'
# ---------------------

# Cache for follower count
cache = {
    'count': 854, # Last known verified count as fallback
    'last_updated': int(time.time())
}

def get_instagram_followers(username):
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "x-ig-app-id": "936619743392459",
    }
    
    if SESSIONID:
        headers["Cookie"] = f"sessionid={SESSIONID}"
    
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

def follower_polling_thread():
    """Background thread that polls Instagram every 30 seconds and emits via WebSocket."""
    print("Background polling thread started.")
    while True:
        new_count = get_instagram_followers(USERNAME)
        if new_count is not None:
            cache['count'] = new_count
            cache['last_updated'] = int(time.time())
            print(f"Polling: {USERNAME} has {new_count} followers.")
            
            # Emit to all connected clients
            socketio.emit('follower_update', {
                'username': USERNAME,
                'count': cache['count'],
                'last_updated': cache['last_updated']
            })
        
        # Wait for 30 seconds before next poll
        socketio.sleep(30)

@app.route('/api/followers')
def followers():
    return jsonify({
        'username': USERNAME,
        'count': cache['count'],
        'last_updated': cache['last_updated']
    })

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Send current count immediately on connect
    emit('follower_update', {
        'username': USERNAME,
        'count': cache['count'],
        'last_updated': cache['last_updated']
    })

if __name__ == '__main__':
    # Initial fetch
    initial_count = get_instagram_followers(USERNAME)
    if initial_count:
        cache['count'] = initial_count
        cache['last_updated'] = int(time.time())
    
    # Start background thread
    socketio.start_background_task(follower_polling_thread)
    
    print(f"Starting Gulf Tech Follower Counter Server on http://localhost:5555")
    socketio.run(app, host='0.0.0.0', port=5555, debug=False)
