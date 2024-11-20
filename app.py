from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.json
        video_url = data.get("video_url")
        
        # Send initial response to acknowledge request receipt
        if not video_url:
            return jsonify({"error": "Video URL not provided"}), 400

        ydl_opts = {
            'outtmpl': 'downloaded_video.mp4',
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # After downloading, return a success response
        return jsonify({"message": "Video downloaded successfully", "file_path": "downloaded_video.mp4"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
