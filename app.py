from flask import Flask, request, send_file
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('video_url')
    
    try:
        # yt-dlp options
        ydl_opts = {
            'outtmpl': 'downloaded_video.mp4',
            'format': 'bestvideo+bestaudio/best',
        }

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Send the file back to the client
        return send_file('downloaded_video.mp4', as_attachment=True)

    except Exception as e:
        return {"message": f"Error: {str(e)}"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
