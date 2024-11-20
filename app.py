from flask import Flask, request, jsonify
from google.cloud import storage
import os

app = Flask(__name__)

# Set up Google Cloud credentials (make sure your JSON file is set up properly in Render)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/secrets/keyfile.json"

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

# Replace this with your Google Cloud Storage bucket name
BUCKET_NAME = 'your_bucket_name_here'

@app.route('/')
def home():
    return "YouTube Video Uploader is Running"

@app.route('/download', methods=['POST'])
def download():
    try:
        # Get the incoming JSON request data
        data = request.json
        if not data or 'video_url' not in data:
            return jsonify({"error": "Invalid request, 'video_url' is required"}), 400
        
        video_url = data['video_url']

        # Use youtube-dl or yt-dlp to download the video
        video_filename = "downloaded_video.mp4"
        
        os.system(f"yt-dlp -o {video_filename} {video_url}")

        # Upload to Google Cloud Storage
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(video_filename)
        blob.upload_from_filename(video_filename)

        # Delete the local file after upload
        os.remove(video_filename)

        return jsonify({"message": "Video uploaded successfully"}), 200

    except Exception as e:
        # Print error to console for debugging and return an error response
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
