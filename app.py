from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "yt-dlp YouTube API is running"})

@app.route('/getinfo')
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL not provided"}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forcejson': True,
        'extract_flat': False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            return jsonify({
                "title": info.get("title"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),
                "thumbnail": info.get("thumbnail"),
                "formats": [
                    {
                        "format_id": f["format_id"],
                        "ext": f["ext"],
                        "resolution": f.get("height"),
                        "abr": f.get("abr"),
                        "filesize": f.get("filesize"),
                        "url": f["url"],
                        "type": (
                            f["acodec"] + "/" + f["vcodec"]
                            if f["vcodec"] != "none"
                            else "audio"
                        )
                    } for f in formats if f.get("url")
                ]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
