from flask import Flask, render_template, request
import yt_dlp
import os

app = Flask(__name__)

# Função para fazer o download
def download_videos(video_urls):
    options = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'format': 'mp4',
        'writesubtitles': True,
        'subtitleslangs': ['pt', 'en'],
        'allsubtitles': True,
        'subtitles': 'auto',
        'skip_download': False,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            for url in video_urls:
                ydl.download([url])
        return "Todos os downloads foram concluídos!"
    except Exception as e:
        return f"Erro ao baixar os vídeos e legendas: {e}"

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar os downloads
@app.route('/download', methods=['POST'])
def download():
    video_urls = request.form['video_urls'].splitlines()
    result = download_videos(video_urls)
    return result

if __name__ == "__main__":
    app.run(debug=True)
