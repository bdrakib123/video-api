from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "message": "Rakib Video API 🚀 (All Format Auto)"
    })

@app.route("/download")
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,

        # 🔥 ALL FORMAT AUTO SELECT
        'format': 'best/bestvideo+bestaudio/bestvideo/bestaudio',

        # 🍪 cookies (YouTube fix)
        'cookiefile': 'cookies.txt',

        # 🌐 anti-block headers
        'http_headers': {
            'User-Agent': 'Mozilla/5.0'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # 🔗 fallback handling
            video_url = info.get("url")

            # some formats use formats list
            if not video_url and "formats" in info:
                formats = info.get("formats")
                if formats:
                    video_url = formats[-1].get("url")  # last = best fallback

            return jsonify({
                "title": info.get("title"),
                "download_link": video_url,
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader")
            })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
