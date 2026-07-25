from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Song Search & Downloader</title>
    <style>
        * { box-sizing: border-box; }
        body { background-color: #0f0f12; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; padding: 20px; margin: 0; min-height: 100vh; }
        h2 { color: #1db954; font-size: 28px; font-weight: 700; margin-bottom: 20px; }
        input { padding: 14px; width: 70%; max-width: 320px; border-radius: 25px; border: 1px solid #333; background-color: #1a1a20; color: white; font-size: 16px; outline: none; transition: 0.3s; }
        input:focus { border-color: #1db954; }
        button, .btn { padding: 14px 24px; border-radius: 25px; border: none; background-color: #1db954; color: white; font-size: 16px; font-weight: bold; cursor: pointer; text-decoration: none; display: inline-block; transition: 0.3s; margin-left: 5px; }
        button:hover { background-color: #1ed760; transform: scale(1.03); }
        
        .search-form { margin-bottom: 30px; display: flex; justify-content: center; align-items: center; }
        .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
        
        .card { background: #181820; padding: 15px; border-radius: 12px; width: 160px; text-align: center; text-decoration: none; color: white; transition: 0.3s; border: 1px solid #282830; }
        .card:hover { transform: translateY(-5px); background: #22222c; border-color: #1db954; }
        .card img { width: 100%; height: 140px; object-fit: cover; border-radius: 8px; }
        .card p { font-size: 14px; margin-top: 10px; font-weight: 600; word-break: break-word; }
        
        .player-card { background: #181820; max-width: 400px; margin: 0 auto; padding: 25px; border-radius: 16px; text-align: center; border: 1px solid #282830; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .player-card img { width: 100%; max-width: 260px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .player-card h3 { margin: 18px 0 5px; font-size: 22px; color: #fff; }
        .player-card p { color: #aaa; margin-bottom: 20px; font-size: 14px; }
        audio { width: 100%; margin: 15px 0; outline: none; }
        
        .download-title { font-size: 15px; margin-top: 20px; color: #1db954; font-weight: bold; }
        .download-links { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 12px; }
        .dl-btn { background: #22222c; border: 1px solid #1db954; color: #1db954; padding: 8px 16px; border-radius: 20px; font-size: 13px; text-decoration: none; font-weight: bold; transition: 0.3s; }
        .dl-btn:hover { background: #1db954; color: white; }
        
        .back-btn { margin-bottom: 25px; background: #2a2a35; }
        .back-btn:hover { background: #3a3a48; }
    </style>
</head>
<body>

    <h2>🎵 Music Downloader</h2>

    {% if song_detail %}
        <a href="/?q={{ query }}" class="btn back-btn">← Back to Search</a>
        
        <div class="player-card">
            <img src="{{ song_detail.image }}" alt="Cover">
            <h3>{{ song_detail.name }}</h3>
            <p>{{ song_detail.artist }}</p>
            
            {% if song_detail.play_url %}
            <audio controls autoplay>
                <source src="{{ song_detail.play_url }}" type="audio/mp4">
                Your browser does not support audio tag.
            </audio>
            {% endif %}

            <div class="download-title">Download Quality:</div>
            <div class="download-links">
                {% for dl in song_detail.downloadUrl %}
                    <a href="{{ dl.url }}" class="dl-btn" download target="_blank">{{ dl.quality }}</a>
                {% endfor %}
            </div>
        </div>

    {% else %}
        <form method="GET" class="search-form">
            <input type="text" name="q" placeholder="Song ka naam..." value="{{ query }}">
            <button type="submit">Search</button>
        </form>

        <div class="container">
            {% for song in songs %}
            <a href="/song/{{ song.id }}?q={{ query }}" class="card">
                <img src="{{ song.image }}" alt="Song Image">
                <p>{{ song.title }}</p>
            </a>
            {% endfor %}
        </div>
    {% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    query = request.args.get("q", "")
    songs = []
    
    if query:
        api_url = f"https://backend2.listenfree.in/api/search?query={query}"
        try:
            response = requests.get(api_url, headers=HEADERS, timeout=10)
            data = response.json()
            
            if data.get("success") and "data" in data and "songs" in data["data"]:
                results = data["data"]["songs"].get("results", [])
                for item in results:
                    images = item.get("image", [])
                    img_url = images[-1]["url"] if images else ""
                    title = item.get("title", "").replace("&quot;", '"').replace("&#039;", "'")
                    
                    songs.append({
                        "id": item.get("id"),
                        "title": title,
                        "image": img_url
                    })
        except Exception as e:
            print("Search Error:", e)
            
    return render_template_string(HTML_TEMPLATE, songs=songs, query=query, song_detail=None)


@app.route("/song/<song_id>", methods=["GET"])
def song_detail(song_id):
    query = request.args.get("q", "")
    api_url = f"https://backend2.listenfree.in/api/songs/{song_id}"
    song_detail = {}
    
    try:
        response = requests.get(api_url, headers=HEADERS, timeout=10)
        data = response.json()
        
        if data.get("success") and "data" in data and len(data["data"]) > 0:
            song = data["data"][0]
            
            images = song.get("image", [])
            img_url = images[-1]["url"] if images else ""
            
            artists = song.get("artists", {}).get("primary", [])
            artist_name = artists[0]["name"] if artists else ""
            
            download_urls = song.get("downloadUrl", [])
            play_url = download_urls[-1]["url"] if download_urls else ""

            song_detail = {
                "name": song.get("name", "").replace("&quot;", '"').replace("&#039;", "'"),
                "artist": artist_name,
                "image": img_url,
                "play_url": play_url,
                "downloadUrl": download_urls
            }
    except Exception as e:
        print("Detail Error:", e)

    return render_template_string(HTML_TEMPLATE, songs=[], query=query, song_detail=song_detail)
