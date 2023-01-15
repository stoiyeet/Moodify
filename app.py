from deepface import DeepFace
from dotenv import load_dotenv
import json
import os
import base64
from requests import post, get
import pprint

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_playlist(tk, mood):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(tk)
    query = f"?q={mood}&type=playlist&limit=5"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['playlists']


def get_right_playlist(top5, mood):
    for pl in top5['items']:
        if pl['name'] == (mood.capitalize() + " Mix"):
            return pl
    return pl

def get_mood(img_path) -> str:
    face_analysis = DeepFace.analyze(img_path=img_path)
    dominant_emotion = face_analysis['dominant_emotion']
    # print(face_analysis)
    # print('dominant emotion: ',dominant_emotion)
    return dominant_emotion


def main():
    token = get_token()
    img_path = "images/likeAnimals.jpg"
    mood = get_mood(img_path)

    print('mood: ', mood)

    json_result = search_for_playlist(token, mood)
    # print('playlist info: \n')
    # pp = pprint.PrettyPrinter(indent=5)
    # pp.pprint(json_result)

    playlist = get_right_playlist(json_result, mood)
    print(playlist['name'])

if __name__ == '__main__':
    main()
