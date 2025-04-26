from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

# Pasta temporária para salvar vídeos
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_video(url, quality):
    unique_filename = str(uuid.uuid4())  # gera nome único para evitar conflito
    output_template = os.path.join(DOWNLOAD_FOLDER, f"{unique_filename}.%(ext)s")
    
    options = {
        'outtmpl': output_template,
        'format': quality,  # 👈 Agora usando a qualidade escolhida
        'writesubtitles': True,
        'subtitleslangs': ['pt', 'en'],
        'allsubtitles': True,
        'subtitles': 'auto',
        'skip_download': False,
        'cookiefile': 'cookies.txt',  # 👈 Garantindo login via cookies
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_filename = ydl.prepare_filename(info)
        
        if not downloaded_filename.endswith(".mp4"):
            base = os.path.splitext(downloaded_filename)[0]
            downloaded_filename = base + ".mp4"
        
    return downloaded_filename

@app.route('/')
def index():
    return render_templ_
