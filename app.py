from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "message": "Rakib Video API 🚀 (Ultimate Fix)"
    })

@app.route("/download")
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,

        # ❌ NO FORMAT (important)
        # let yt-dlp fetch all formats

        'cookiefile': 'cookies.txt',

        'http_headers': {
            'User-Agent': 'Mozilla/5.0'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            video_url = None

            # ✅ try direct url first
            if info.get("url"):
                video_url = info.get("url")

            # ✅ fallback: pick best format manually
            elif "formats" in info:
                formats = info.get("formats")

                # sort by quality (height)
                formats = sorted(
                    formats,
                    key=lambda x: x.get("height", 0),
                    reverse=True
                )

                for f in formats:
                    if f.get("url"):
                        video_url = f.get("url")
                        break

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
