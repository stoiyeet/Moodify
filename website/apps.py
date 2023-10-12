# website/apps.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename  # Added for secure file handling
from app import SongFinder
import os 
import base64
from io import BytesIO
from werkzeug.datastructures import FileStorage


apps = Blueprint('apps', __name__)

@apps.route('/', methods=['GET', 'POST'])
def find_song():
    pl_url = ""
    mood = ""
    uploaded = False
    if request.method == 'POST':
        image_data = request.form.get('camera_image')
        if image_data:
            header, encoded = image_data.split(",", 1)
            img_bytes = base64.b64decode(encoded)
            file = FileStorage(
                stream=BytesIO(img_bytes),
                filename="captured_image.png",
                content_type="image/png"
            )
        else:
            file = request.files.get('myFile')
        
        if not file or not file.filename:
            flash("No file uploaded. Please select an image.", "error")
        elif file.filename.endswith((".jpg", ".png", ".jpeg")):
            try:
                # Securely save the uploaded file temporarily
                upload_folder = 'uploads'  # Ensure this directory exists or create it
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                
                sf = SongFinder()
                token = sf.get_token()
                mood = sf.get_mood(file_path)  # Fixed: Use the uploaded file's path instead of hardcoded image
                print(f"Detected mood: {mood}")
                
                json_result = sf.search_for_playlist(token, mood)
                playlist = sf.get_right_playlist(json_result, mood)
                if playlist:
                    pl_url = sf.get_url(playlist)
                    print(f"Playlist found: {playlist['name']}")
                    uploaded = True
                else:
                    flash("No matching playlist found. Try a different image.", "error")
                
                # Clean up temporary file
                os.remove(file_path)
            except Exception as e:
                flash(f"An error occurred: {str(e)}", "error")
                print(f"Error during processing: {e}")
        else:
            flash("Invalid file type. Please upload a JPG, PNG, or JPEG.", "error")
    
    return render_template("upload-Page.html", link=pl_url, mood=mood, upload=uploaded)