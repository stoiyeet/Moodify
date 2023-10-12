from deepface import DeepFace
from dotenv import load_dotenv
import json
import os
import base64
from requests import post, get
import re

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

class SongFinder:
    def get_token(self):
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


    def get_auth_header(self, token):
        return {"Authorization": "Bearer " + token}


    def search_for_playlist(self, tk, mood):
        url = "https://api.spotify.com/v1/search"
        headers = self.get_auth_header(tk)
        query = f"?q={mood}&type=playlist&limit=5"

        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)
        return json_result['playlists']


    def get_right_playlist(self, playlists, mood):
        """Find the best matching playlist for the mood"""
        # First try to find an exact match with the mood name
        for pl in playlists['items']:
            if pl and mood.lower() in pl['name'].lower():
                return pl
                
        # If no exact match, return the first playlist
        if playlists['items']:
            return playlists['items'][0]
        return None

    def get_url(self, pl_info):
        return pl_info['external_urls']['spotify']


    def get_mood(self, img_path) -> str:
        """Analyze the image for dominant emotion using DeepFace."""
        try:
            face_analysis = DeepFace.analyze(img_path=img_path, actions=['emotion'])  # Optimized: Specify actions for efficiency
            if not face_analysis:
                raise ValueError("No face detected in the image.")
            dominant_emotion = face_analysis[0]['dominant_emotion']
            print(f"Image path: {img_path}, Dominant emotion: {dominant_emotion}")
            return dominant_emotion
        except Exception as e:
            print(f"Error in mood detection: {e}")
            return "neutral"  # Fallback to avoid crashes; can be customized


def main():
    sf = SongFinder()
    token = sf.get_token()
    # img_path = "images/likeAnimals.jpg"
    img_path = "images/ashisw.jpg"
    mood = sf.get_mood(img_path)

    print('mood of mine: ', mood)

    json_result = sf.search_for_playlist(token, mood)
    # print('playlist info: \n')
    # pp = pprint.PrettyPrinter(indent=5)
    # pp.pprint(json_result)

    playlist = sf.get_right_playlist(json_result, mood)
    print('playlist name: ', playlist['name'])

    pl_url = sf.get_url(playlist)
    print('playlist url: ', pl_url)



if __name__ == '__main__':
    main()