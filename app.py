from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Get the YouTube URL from the request
        data = request.get_json()
        youtube_url = data.get("video_url")
        
        if not youtube_url:
            return jsonify({"error": "No video URL provided"}), 400
        
        # Download video using yt-dlp
        result = subprocess.run([
            'yt-dlp',
            youtube_url,
            '--cookies', 'youtube_cookies.txt',
            '-o', 'downloaded_video.mp4'
        ], text=True, capture_output=True)

        if result.returncode != 0:
            # Log and return the error from yt-dlp
            return jsonify({"error": result.stderr}), 500

        return jsonify({"message": "Video downloaded successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
