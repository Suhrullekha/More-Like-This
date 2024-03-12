from dotenv import load_dotenv
import os 
import base64
from requests import post, get
import json

load_dotenv()#loads the env files
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#print(client_id,client_secret)

def get_token(): 
    #create an auth string encoded in base 64
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic "+auth_base64, 
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token): 
    return {"Authorization": "Bearer "+token} #

def search_for_artist(token, artist_name): #returns all info under the artist like followers, albums, tracks etc
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1" #can also do artist,track... and returns top #1 artist
    query_url = url + query
    result = get(query_url,  headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No Artist Found")
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id): #returns the specified artist's top tracks
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


##########ADDED FUNCTIONS 

#use Search for Item by song artist to find artist id, track id and genre
def search_for_song(token, track, artist_name): 
    url = "https://api.spotify.com/v1/search" 
    #url = "https://api.spotify.com/v1/search?q=remaster%2520track%3ADoxy%2520artist%3AMiles%2520Davis&type=track%2Cartist"
    headers = get_auth_header(token)
    query = f"?q={track}{artist_name}&type=track&artist&limit=1" #can also do artist,track... and returns top #1 artist
    query_url = url + query
    result = get(query_url,  headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No Song Found")
        return None
    return json_result[0] 

#use get track audio features to get energy, dancability...
def get_track_info(token, track_id): 
    url = "https://api.spotify.com/v1/audio-features/{id}" 

#use all the info collected to find the recommended songs 
def get_recommendations(token, artist_id, track_id, genre): 
    url = "https://api.spotify.com/v1/recommendations"





    

token = get_token()
artist = search_for_artist(token, "ACDC")
artist_id = artist["id"]
songs = get_songs_by_artist(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")
