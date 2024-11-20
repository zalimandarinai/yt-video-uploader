import os
import subprocess
from flask import Flask, request
from google.cloud import storage

app = Flask(__name__)
BUCKET_NAME = 'YOUR_BUCKET_NAME'

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.json.get('video_url')
    if not video_url:
        return "No video URL provided", 400

    # Download video with yt-dlp
    file_name = 'video.mp4'
    subprocess.run(['yt-dlp', '-o', file_name, video_url])

    # Upload to Google Cloud Storage
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)

    # Clean up local file
    os.remove(file_name)

    return f"Uploaded {file_name} to {BUCKET_NAME}", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
