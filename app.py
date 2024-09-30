from os import access

import flask
import requests
from flask import Flask, request, redirect, session
import webbrowser
import Posterfy


app = Flask(__name__)

# Replace these with your actual Spotify app credentials
CLIENT_ID = 'a2b8b16af30f4e1f9bf9b5a86ee8862b'
CLIENT_SECRET = '877d125158854158b128e63d13a7cfdb'
REDIRECT_URI = 'http://localhost:8888/callback'
app.secret_key = 'my_secret_key'

# Step 1: Get the authorization URL
@app.route('/')
def login():
    # make sure to add scope here whenever necessary.
    # to read the top tracks of a person, the access_token must have scope top-user-read
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=user-read-private user-read-email user-top-read"
    return redirect(auth_url)

# Step 2: Handle the callback and exchange code for token
@app.route('/callback', methods=["POST", "GET"])
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
    session['access_token'] = access_token

    return flask.render_template("home.html")

@app.route('/poster', methods=["POST", "GET"])
def poster():
    access_token = session.get('access_token')
    artist_album = flask.request.form['art_alb_tra'].lower() # for now we can say that the user is always inputting artist or album.
    top_songs = requests.get(
        'https://api.spotify.com/v1/me/top/tracks?limit=50',
        headers={'Authorization': f'Bearer {access_token}'}
    ).json()

    # getting music collage
    song_images = get_song_images(top_songs)
    img_base64 = Posterfy.create_square_collage(song_images, artist_album)

    return flask.render_template(
        "poster.html",
        img_base64=img_base64
    )

def get_song_images(top_songs):
    song_images = {}

    for song in range(len(top_songs['items'])):
        this_song = top_songs['items'][song]
        this_album_name = top_songs['items'][song]['album']['name'].lower()
        this_image = this_song['album']['images'][0]['url']
        this_artist = top_songs['items'][song]['artists'][0]['name'].lower()
        this_track = top_songs['items'][song]['name'].lower()

        song_images[song] = [this_album_name, this_artist, this_track, this_image]

    return song_images

if __name__ == '__main__':
    webbrowser.open('http://localhost:8888/')
    app.run(port=8888)



# things I want to ensure
"""
Depending on how many album covers we add, we need to make sure we have that many unique albums, or not depending on that users preference
"""