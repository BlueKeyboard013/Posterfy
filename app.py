from os import access

import requests
from flask import Flask, request, redirect
import webbrowser

app = Flask(__name__)

# Replace these with your actual Spotify app credentials
CLIENT_ID = 'a2b8b16af30f4e1f9bf9b5a86ee8862b'
CLIENT_SECRET = '877d125158854158b128e63d13a7cfdb'
REDIRECT_URI = 'http://localhost:8888/callback'

# Step 1: Get the authorization URL
@app.route('/')
def login():
    # make sure to add scope here whenever necessary.
    # to read the top tracks of a person, the access_token must have scope top-user-read
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=user-read-private user-read-email user-top-read"
    return redirect(auth_url)

# Step 2: Handle the callback and exchange code for token
@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'

    response = requests.post(token_url, {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    token_info = response.json()
    access_token = token_info['access_token']

    print(token_info)

    # Now you can use the access token to make API calls

    top_songs = requests.get(
        'https://api.spotify.com/v1/me/top/tracks?limit=50',
        headers={'Authorization': f'Bearer {access_token}'}
    ).json()


    # print(top_songs['items'][1]['album']['images'])
    # print(len(top_songs['items']))

    song_images = []

    for song in range(len(top_songs['items'])):
        curr_song = top_songs['items'][song]
        song_images.append(curr_song['album']['images'][0]['url'])

    for url in song_images:
        print(url)


    return f'Top songs: {top_songs}'

if __name__ == '__main__':
    webbrowser.open('http://localhost:8888/')
    app.run(port=8888)
