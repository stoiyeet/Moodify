# from deepface import DeepFace
# from dotenv import load_dotenv
import json
import os
import base64
# from requests import post, get
import pprint
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import songFinder

# load_dotenv()

# client_id = os.getenv("CLIENT_ID")
# client_secret = os.getenv("CLIENT_SECRET")
apps = Blueprint('apps', __name__)


@apps.route('/', methods=['GET', 'POST'])
def apps():
    if request.method == 'POST':
        file = request.form.get('myFile')
        # txt = request.form.get('faker')
        # print(file.endswith(".jpg"))
        if file.endswith(".jpg"):
            sf = songFinder(file)
            token = sf.get_token()
            mood = sf.get_mood(file)
            print("Mood: ", mood)
            json_result = sf.search_for_playlist(token, mood)
            playlist = sf.get_right_playlist(json_result, mood)
            print(playlist['name'])
        # face_analysis = DeepFace.analyze(img_path=file)
        # dominant_emotion = face_analysis['dominant_emotion']
        # print(face_analysis)
        # print(dominant_emotion)
        # return render_template("upload-Page.html", d=dominant_emotion)
    return render_template("upload-Page.html")
