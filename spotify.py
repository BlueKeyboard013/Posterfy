import requests
import base64

## Steps:
"""
Make a call to spotify to first get the access token.
Then use this token when making calls to other endpoints (artists, albums, etc.) so that the call
    can be authenticated.
token lasts for 1 hour.
that's it.
"""

# Your Spotify API credentials
client_id = 'a2b8b16af30f4e1f9bf9b5a86ee8862b'
client_secret = '877d125158854158b128e63d13a7cfdb'

# Step 1: Get access token
auth_url = 'https://accounts.spotify.com/api/token'
credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

response = requests.post(
    auth_url,
    headers={
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    data={
        'grant_type': 'client_credentials'
    }
)

token_info = response.json()
access_token = token_info['access_token']
print(access_token)
print("------------------------------------")

# Step 2: Make an API call (e.g., get artist info)
artist_id = '3vK0AN7hAMXqekxH3HdtFp'  # Replace with actual artist ID
# api_url = f'https://api.spotify.com/v1/artists/{artist_id}'
api_url = 'https://api.spotify.com/v1/me'

response = requests.get(
    api_url,
    headers={
        'Authorization': f'Bearer {access_token}'
    }
)

artist_info = response.json()
print(artist_info)

# artist gives back a 640 x 640 picture (of something, i dont really know exactly, i think the artist profile pic)
