from flask import Flask, render_template_string, request, Response
import requests

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Melodify | Premium Music Downloader</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0e1a;
            --bg-secondary: #111827;
            --bg-card: rgba(20, 30, 50, 0.75);
            --accent-1: #6ee7b7;
            --accent-2: #3b82f6;
            --accent-3: #8b5cf6;
            --gradient-main: linear-gradient(135deg, #6ee7b7, #3b82f6, #8b5cf6);
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --glass-border: rgba(255, 255, 255, 0.08);
            --shadow-glow: 0 8px 32px rgba(59, 130, 246, 0.15);
            --radius-sm: 12px;
            --radius-md: 18px;
            --radius-lg: 28px;
            --transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 25px 20px 40px;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-image: 
                radial-gradient(ellipse at 20% 50%, rgba(59, 130, 246, 0.06) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 20%, rgba(139, 92, 246, 0.06) 0%, transparent 60%),
                radial-gradient(ellipse at 50% 100%, rgba(110, 231, 183, 0.04) 0%, transparent 50%);
        }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--accent-2); border-radius: 20px; }

        @keyframes fadeSlideUp {
            from { opacity: 0; transform: translateY(25px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes spinSlow {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            animation: fadeSlideUp 0.6s ease-out;
        }
        .header .logo {
            display: inline-flex;
            align-items: center;
            gap: 14px;
            font-size: 34px;
            font-weight: 800;
            background: var(--gradient-main);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -1px;
        }
        .header .logo i {
            font-size: 36px;
            background: var(--gradient-main);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 20px rgba(110, 231, 183, 0.3));
        }
        .header .subtitle {
            color: var(--text-secondary);
            font-size: 14px;
            font-weight: 500;
            margin-top: 4px;
            letter-spacing: 0.5px;
        }
        .header .subtitle span {
            color: var(--accent-1);
            -webkit-text-fill-color: var(--accent-1);
        }

        .search-wrapper {
            width: 100%;
            max-width: 520px;
            margin-bottom: 28px;
            animation: fadeSlideUp 0.7s ease-out;
        }
        .search-box {
            display: flex;
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 60px;
            padding: 4px 4px 4px 22px;
            box-shadow: var(--shadow-glow);
            transition: var(--transition);
        }
        .search-box:focus-within {
            border-color: rgba(110, 231, 183, 0.4);
            box-shadow: 0 8px 40px rgba(59, 130, 246, 0.2);
            transform: scale(1.01);
        }
        .search-box input {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: var(--text-primary);
            font-size: 15px;
            font-weight: 500;
            padding: 14px 0;
            font-family: inherit;
        }
        .search-box input::placeholder {
            color: var(--text-muted);
            font-weight: 400;
        }
        .search-box button {
            background: var(--gradient-main);
            border: none;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            color: #000;
            font-size: 18px;
            cursor: pointer;
            transition: var(--transition);
            box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .search-box button:hover {
            transform: scale(1.07) rotate(5deg);
            box-shadow: 0 6px 30px rgba(59, 130, 246, 0.5);
        }

        .back-btn {
            align-self: flex-start;
            max-width: 520px;
            width: 100%;
            margin-bottom: 16px;
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: var(--transition);
            padding: 6px 0;
        }
        .back-btn:hover { color: var(--accent-1); }
        .back-btn:hover i { transform: translateX(-4px); }

        .grid-container {
            width: 100%;
            max-width: 600px;
            animation: fadeSlideUp 0.8s ease-out;
        }
        .grid-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            padding: 0 4px;
        }
        .grid-header h3 {
            font-size: 16px;
            font-weight: 600;
            color: var(--text-secondary);
        }
        .grid-header .result-count {
            font-size: 12px;
            color: var(--text-muted);
            background: var(--bg-card);
            padding: 4px 14px;
            border-radius: 20px;
            border: 1px solid var(--glass-border);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 16px;
        }

        .card {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-md);
            padding: 12px 12px 14px;
            text-decoration: none;
            color: var(--text-primary);
            transition: var(--transition);
            text-align: center;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .card::before {
            content: '';
            position: absolute;
            inset: 0;
            background: var(--gradient-main);
            opacity: 0;
            transition: var(--transition);
            border-radius: inherit;
            z-index: 0;
        }
        .card:hover {
            transform: translateY(-6px) scale(1.02);
            border-color: rgba(110, 231, 183, 0.25);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        }
        .card:hover::before { opacity: 0.06; }
        .card > * { position: relative; z-index: 1; }
        .card img {
            width: 100%;
            aspect-ratio: 1/1;
            object-fit: cover;
            border-radius: var(--radius-sm);
            margin-bottom: 10px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
            transition: var(--transition);
        }
        .card:hover img { transform: scale(1.03); }
        .card .card-title {
            font-size: 13px;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            line-height: 1.3;
        }
        .card .card-artist {
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 500;
            margin-top: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .card .play-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(8px);
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: var(--transition);
            border: 2px solid rgba(255, 255, 255, 0.15);
            z-index: 2;
        }
        .card:hover .play-overlay { opacity: 1; }
        .card .play-overlay i { color: white; font-size: 18px; }

        .empty-state {
            text-align: center;
            padding: 50px 20px;
            color: var(--text-secondary);
            grid-column: 1/-1;
        }
        .empty-state i {
            font-size: 52px;
            color: var(--text-muted);
            margin-bottom: 16px;
            opacity: 0.3;
        }
        .empty-state h4 { font-size: 18px; font-weight: 600; margin-bottom: 6px; color: var(--text-primary); }
        .empty-state p { font-size: 14px; color: var(--text-muted); }

        .player-wrapper {
            width: 100%;
            max-width: 400px;
            animation: fadeSlideUp 0.6s ease-out;
        }
        .player-card {
            background: var(--bg-card);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            padding: 30px 28px 28px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }
        .player-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 30% 20%, rgba(110, 231, 183, 0.04), transparent 50%);
            pointer-events: none;
        }
        .player-card > * { position: relative; z-index: 1; }

        .album-art {
            width: 210px;
            height: 210px;
            border-radius: var(--radius-md);
            object-fit: cover;
            margin-bottom: 18px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
            transition: var(--transition);
        }
        .album-art.playing { animation: spinSlow 8s linear infinite; }

        .song-title {
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 2px;
            letter-spacing: -0.3px;
        }
        .artist-name {
            font-size: 15px;
            color: var(--text-secondary);
            font-weight: 500;
            margin-bottom: 20px;
        }

        .progress-area {
            margin-bottom: 18px;
            padding: 0 2px;
        }
        .progress-bar {
            width: 100%;
            height: 5px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .progress {
            width: 0%;
            height: 100%;
            background: var(--gradient-main);
            border-radius: 10px;
            transition: width 0.08s linear;
        }
        .time-stamps {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 500;
            margin-top: 6px;
        }

        .controls {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 22px;
            margin-bottom: 22px;
        }
        .controls .ctrl-btn {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-size: 18px;
            cursor: pointer;
            transition: var(--transition);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .controls .ctrl-btn:hover {
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.05);
        }
        .play-btn {
            width: 60px !important;
            height: 60px !important;
            border-radius: 50%;
            background: var(--gradient-main) !important;
            border: none !important;
            color: #000 !important;
            font-size: 22px !important;
            cursor: pointer;
            box-shadow: 0 4px 30px rgba(59, 130, 246, 0.35);
            transition: var(--transition);
        }
        .play-btn:hover {
            transform: scale(1.08) !important;
            box-shadow: 0 8px 45px rgba(59, 130, 246, 0.5) !important;
        }

        .download-trigger-btn {
            width: 100%;
            padding: 14px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(110, 231, 183, 0.3);
            border-radius: var(--radius-sm);
            color: var(--accent-1);
            font-weight: 700;
            font-size: 15px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            transition: var(--transition);
            font-family: inherit;
        }
        .download-trigger-btn:hover {
            background: var(--gradient-main);
            color: #000;
            border-color: transparent;
            box-shadow: 0 4px 30px rgba(110, 231, 183, 0.3);
            transform: translateY(-2px);
        }

        .modal {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            align-items: center;
            justify-content: center;
            z-index: 1000;
            animation: fadeSlideUp 0.3s ease-out;
        }
        .modal-content {
            background: var(--bg-secondary);
            border: 1px solid var(--glass-border);
            padding: 28px 24px 22px;
            border-radius: var(--radius-md);
            width: 90%;
            max-width: 340px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
        }
        .modal-content h4 {
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 6px;
        }
        .modal-content .modal-sub {
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 18px;
        }
        .quality-btn {
            display: block;
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--glass-border);
            color: var(--text-primary);
            border-radius: var(--radius-sm);
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
            transition: var(--transition);
            font-family: inherit;
        }
        .quality-btn i { margin-right: 10px; color: var(--accent-1); }
        .quality-btn:hover {
            background: var(--gradient-main);
            color: #000;
            border-color: transparent;
            transform: scale(1.02);
        }
        .quality-btn:hover i { color: #000; }
        .close-btn {
            margin-top: 14px;
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            padding: 8px 16px;
            transition: var(--transition);
            font-family: inherit;
        }
        .close-btn:hover { color: var(--text-primary); }

        .toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%) translateY(80px);
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            padding: 12px 24px;
            border-radius: 60px;
            font-size: 13px;
            font-weight: 500;
            color: var(--text-primary);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
            opacity: 0;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 2000;
            pointer-events: none;
        }
        .toast.show {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
        .toast i { margin-right: 10px; color: var(--accent-1); }

        @media (max-width: 480px) {
            body { padding: 16px 12px 30px; }
            .header .logo { font-size: 26px; }
            .search-box { padding: 3px 3px 3px 16px; }
            .search-box input { font-size: 14px; padding: 12px 0; }
            .search-box button { width: 44px; height: 44px; font-size: 16px; }
            .grid { grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 12px; }
            .album-art { width: 160px; height: 160px; }
            .player-card { padding: 22px 18px 20px; }
            .song-title { font-size: 17px; }
        }
        @media (max-width: 380px) {
            .grid { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>

    <header class="header">
        <div class="logo">
            <i class="fa-solid fa-headphones"></i> Melodify
        </div>
        <p class="subtitle">🎧 Discover &amp; download <span>high-quality</span> music</p>
    </header>

    {% if song_detail %}

        <div class="player-wrapper">
            <a href="/?q={{ query }}" class="back-btn"><i class="fa-solid fa-arrow-left"></i> Back to search</a>
            
            <div class="player-card">
                <img src="{{ song_detail.image }}" alt="Cover" class="album-art" id="albumArt">
                <div class="song-title">{{ song_detail.name }}</div>
                <div class="artist-name">{{ song_detail.artist }}</div>

                <audio id="audio-element" src="{{ song_detail.play_url }}" preload="metadata"></audio>

                <div class="progress-area">
                    <div class="progress-bar" id="progress-bar">
                        <div class="progress" id="progress"></div>
                    </div>
                    <div class="time-stamps">
                        <span id="current-time">0:00</span>
                        <span id="duration">0:00</span>
                    </div>
                </div>

                <div class="controls">
                    <button class="ctrl-btn" id="prevBtn"><i class="fa-solid fa-backward"></i></button>
                    <button class="play-btn" id="play-btn"><i class="fa-solid fa-play"></i></button>
                    <button class="ctrl-btn" id="nextBtn"><i class="fa-solid fa-forward"></i></button>
                </div>

                <button class="download-trigger-btn" onclick="openModal()">
                    <i class="fa-solid fa-download"></i> Download Song
                </button>
            </div>
        </div>

        <div class="modal" id="downloadModal">
            <div class="modal-content">
                <h4>⬇️ Choose Quality</h4>
                <p class="modal-sub">Select your preferred bitrate</p>
                {% for dl in song_detail.downloadUrl %}
                    <a href="/download?url={{ dl.url | urlencode }}&name={{ song_detail.name | urlencode }} - {{ song_detail.artist | urlencode }}.mp3" class="quality-btn">
                        <i class="fa-solid fa-circle"></i> {{ dl.quality }}
                    </a>
                {% endfor %}
                <button class="close-btn" onclick="closeModal()">Cancel</button>
            </div>
        </div>

    {% else %}

        <div class="search-wrapper">
            <form method="GET" class="search-box">
                <input type="text" name="q" placeholder="Search songs, artists, albums..." value="{{ query }}" required autofocus>
                <button type="submit"><i class="fa-solid fa-magnifying-glass"></i></button>
            </form>
        </div>

        <div class="grid-container">
            <div class="grid-header">
                <h3>{% if query %}Results{% else %}Trending 🔥{% endif %}</h3>
                {% if songs %}<span class="result-count">{{ songs|length }} songs</span>{% endif %}
            </div>

            <div class="grid">
                {% if songs %}
                    {% for song in songs %}
                    <a href="/song/{{ song.id }}?q={{ query }}" class="card">
                        <img src="{{ song.image }}" alt="{{ song.title }}" loading="lazy">
                        <div class="play-overlay"><i class="fa-solid fa-play"></i></div>
                        <div class="card-title">{{ song.title }}</div>
                        <div class="card-artist">{{ song.artist or 'Unknown' }}</div>
                    </a>
                    {% endfor %}
                {% else %}
                    <div class="empty-state">
                        <i class="fa-solid fa-music-slash"></i>
                        <h4>{% if query %}No results found{% else %}Start searching!{% endif %}</h4>
                        <p>{% if query %}Try a different keyword or artist name{% else %}Type a song name above ✨{% endif %}</p>
                    </div>
                {% endif %}
            </div>
        </div>

    {% endif %}

    <div class="toast" id="toast"><i class="fa-solid fa-check-circle"></i> <span id="toastMsg">Ready</span></div>

    <script>
    const audio = document.getElementById('audio-element');
    const playBtn = document.getElementById('play-btn');
    const progressBar = document.getElementById('progress-bar');
    const progress = document.getElementById('progress');
    const currentTimeEl = document.getElementById('current-time');
    const durationEl = document.getElementById('duration');
    const albumArt = document.getElementById('albumArt');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    // ===== SONG QUEUE (temporary) =====
    let songQueue = [];
    let currentIndex = 0;

    // ===== INITIALIZE =====
    if (audio) {
        // ❌ AUTO-PLAY HATAYA - ab user manually play karega
        // audio.play().catch(() => {});

        // Play/Pause
        playBtn.addEventListener('click', () => {
            if (audio.paused) {
                audio.play();
                playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
                albumArt.classList.add('playing');
            } else {
                audio.pause();
                playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
                albumArt.classList.remove('playing');
            }
        });

        // Update progress
        audio.addEventListener('timeupdate', () => {
            const { currentTime, duration } = audio;
            if (duration) {
                progress.style.width = `${(currentTime / duration) * 100}%`;
                currentTimeEl.textContent = formatTime(currentTime);
                durationEl.textContent = formatTime(duration);
            }
        });

        // Seek
        progressBar.addEventListener('click', (e) => {
            const rect = progressBar.getBoundingClientRect();
            audio.currentTime = ((e.clientX - rect.left) / rect.width) * audio.duration;
        });

        // Song ended
        audio.addEventListener('ended', () => {
            playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
            albumArt.classList.remove('playing');
            progress.style.width = '0%';
            currentTimeEl.textContent = '0:00';
            showToast('⏭️ Song ended');
            
            // Auto-play next if available
            if (songQueue.length > 0) {
                setTimeout(() => {
                    nextSong();
                }, 1500);
            }
        });

        // Format time
        function formatTime(seconds) {
            if (!seconds || isNaN(seconds)) return '0:00';
            const m = Math.floor(seconds / 60);
            const s = Math.floor(seconds % 60);
            return `${m}:${s < 10 ? '0' : ''}${s}`;
        }

        // Load metadata
        audio.addEventListener('loadedmetadata', () => {
            durationEl.textContent = formatTime(audio.duration);
        });

        // ===== NEXT / PREV BUTTONS =====
        prevBtn.addEventListener('click', () => {
            if (songQueue.length > 0) {
                currentIndex = (currentIndex - 1 + songQueue.length) % songQueue.length;
                loadSong(currentIndex);
            } else {
                showToast('⛔ No previous song');
            }
        });

        nextBtn.addEventListener('click', nextSong);

        function nextSong() {
            if (songQueue.length > 0) {
                currentIndex = (currentIndex + 1) % songQueue.length;
                loadSong(currentIndex);
            } else {
                showToast('⛔ No next song');
            }
        }

        function loadSong(index) {
            const song = songQueue[index];
            if (!song) return;
            
            // Update UI
            document.querySelector('.song-title').textContent = song.name;
            document.querySelector('.artist-name').textContent = song.artist;
            document.getElementById('albumArt').src = song.image;
            
            // Update audio
            audio.src = song.play_url;
            audio.load();
            
            // Auto-play
            audio.play().then(() => {
                playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
                albumArt.classList.add('playing');
                showToast(`🎵 Now playing: ${song.name}`);
            }).catch(() => {
                playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
                albumArt.classList.remove('playing');
            });
        }

        // ===== COLLECT QUEUE FROM SEARCH RESULTS =====
        // This runs when page loads and there are search results
        function loadQueueFromSearch() {
            const cards = document.querySelectorAll('.card');
            const queue = [];
            
            cards.forEach(card => {
                const href = card.getAttribute('href');
                if (href && href.startsWith('/song/')) {
                    const id = href.split('/')[2].split('?')[0];
                    const title = card.querySelector('.card-title')?.textContent || '';
                    const artist = card.querySelector('.card-artist')?.textContent || 'Unknown';
                    const image = card.querySelector('img')?.src || '';
                    
                    // We'll fetch actual data when needed
                    queue.push({ id, name: title, artist, image, play_url: '' });
                }
            });
            
            // Store for later use
            window.songQueueData = queue;
            
            // Update queue for current song
            if (queue.length > 0) {
                songQueue = queue;
                // Try to find current song in queue
                const currentTitle = document.querySelector('.song-title')?.textContent || '';
                const foundIndex = queue.findIndex(s => s.name === currentTitle);
                if (foundIndex !== -1) {
                    currentIndex = foundIndex;
                    // Add play_url to current song
                    if (audio) {
                        queue[foundIndex].play_url = audio.src;
                    }
                }
            }
        }

        // Call after page load
        if (document.querySelector('.card')) {
            setTimeout(loadQueueFromSearch, 500);
        }

        // ===== OVERRIDE CARD CLICKS TO ADD TO QUEUE =====
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href && href.startsWith('/song/')) {
                    e.preventDefault();
                    const songId = href.split('/')[2].split('?')[0];
                    const title = this.querySelector('.card-title')?.textContent || '';
                    const artist = this.querySelector('.card-artist')?.textContent || 'Unknown';
                    const image = this.querySelector('img')?.src || '';
                    
                    // Add to queue
                    const songData = { id: songId, name: title, artist, image, play_url: '' };
                    
                    // Check if already in queue
                    const existing = songQueue.findIndex(s => s.id === songId);
                    if (existing === -1) {
                        songQueue.push(songData);
                        currentIndex = songQueue.length - 1;
                    } else {
                        currentIndex = existing;
                    }
                    
                    // Fetch actual song details
                    fetchSongDetails(songId, (data) => {
                        if (data) {
                            songQueue[currentIndex] = data;
                            loadSong(currentIndex);
                        }
                    });
                }
            });
        });

        // ===== FETCH SONG DETAILS =====
        function fetchSongDetails(songId, callback) {
            fetch(`/song/${songId}?q=${encodeURIComponent(document.querySelector('input[name="q"]')?.value || '')}`)
                .then(response => response.text())
                .then(html => {
                    // Parse the HTML to get song details
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    
                    const name = doc.querySelector('.song-title')?.textContent || '';
                    const artist = doc.querySelector('.artist-name')?.textContent || 'Unknown';
                    const image = doc.querySelector('.album-art')?.src || '';
                    const play_url = doc.querySelector('#audio-element')?.src || '';
                    
                    callback({ id: songId, name, artist, image, play_url });
                })
                .catch(() => {
                    callback(null);
                });
        }
    }

    // ===== MODAL FUNCTIONS =====
    function openModal() {
        document.getElementById('downloadModal').style.display = 'flex';
    }
    function closeModal() {
        document.getElementById('downloadModal').style.display = 'none';
    }
    document.getElementById('downloadModal')?.addEventListener('click', (e) => {
        if (e.target === e.currentTarget) closeModal();
    });

    // ===== TOAST =====
    function showToast(msg) {
        const toast = document.getElementById('toast');
        document.getElementById('toastMsg').textContent = msg;
        toast.classList.add('show');
        clearTimeout(toast._timeout);
        toast._timeout = setTimeout(() => toast.classList.remove('show'), 3000);
    }

    // ===== KEYBOARD SHORTCUTS =====
    document.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT') return;
        if (e.code === 'Space' && audio) {
            e.preventDefault();
            playBtn.click();
        }
        if (e.code === 'ArrowRight' && audio) {
            e.preventDefault();
            audio.currentTime = Math.min(audio.currentTime + 5, audio.duration);
        }
        if (e.code === 'ArrowLeft' && audio) {
            e.preventDefault();
            audio.currentTime = Math.max(audio.currentTime - 5, 0);
        }
        if (e.code === 'Escape') closeModal();
        if (e.code === 'KeyN' && audio) {
            e.preventDefault();
            nextBtn.click();
        }
        if (e.code === 'KeyP' && audio) {
            e.preventDefault();
            prevBtn.click();
        }
    });

    // ===== INIT =====
    if (document.querySelector('.player-card')) {
        // Don't show auto-play toast
        // setTimeout(() => showToast('🎵 Click play to start'), 400);
        
        // Add current song to queue
        const currentTitle = document.querySelector('.song-title')?.textContent || '';
        const currentArtist = document.querySelector('.artist-name')?.textContent || '';
        const currentImage = document.querySelector('.album-art')?.src || '';
        const currentUrl = audio?.src || '';
        
        if (currentTitle) {
            songQueue.push({
                id: 'current',
                name: currentTitle,
                artist: currentArtist,
                image: currentImage,
                play_url: currentUrl
            });
            currentIndex = 0;
        }
    }
</script>
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
                    
                    artists = item.get("artists", {}).get("primary", [])
                    artist_name = artists[0]["name"] if artists else "Unknown"
                    
                    songs.append({
                        "id": item.get("id"),
                        "title": title,
                        "image": img_url,
                        "artist": artist_name
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
            artist_name = artists[0]["name"] if artists else "Unknown Artist"
            
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

@app.route("/download")
def download_file():
    file_url = request.args.get("url")
    custom_name = request.args.get("name", "song.mp3")
    
    req = requests.get(file_url, headers=HEADERS, stream=True)
    
    response = Response(req.iter_content(chunk_size=1024), content_type=req.headers.get('content-type'))
    response.headers['Content-Disposition'] = f'attachment; filename="{custom_name}"'
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)