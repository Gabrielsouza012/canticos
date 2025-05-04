from flask import Flask, render_template, request, send_file
import yt_dlp
from yt_dlp.utils import DownloadError
import os
import re
import uuid
import subprocess

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_video(url):
    print("🔧 Verificando ambiente...")
    print("[yt-dlp version]", subprocess.getoutput("yt-dlp --version"))
    print("[ffmpeg version]", subprocess.getoutput("ffmpeg -version"))

    unique_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_FOLDER, f"%(title)s_{unique_id}.%(ext)s")

    options = {
        'outtmpl': output_template,
        'format': 'best',  # formato mais simples e compatível
        'noplaylist': True,
        'logger': yt_dlp.utils.std_logger(),
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('video_urls', '').strip()

    if not url:
        return "Nenhum link enviado.", 400

    try:
        video_path = download_video(url)
        response = send_file(video_path, as_attachment=True)
        # os.remove(video_path)  # opcional: apagar após download
        return response
    except DownloadError as e:
        print(f"[yt-dlp ERROR] {e}")
        return "Erro: vídeo indisponível ou restrito.", 400
    except Exception as e:
        print(f"[GENERIC ERROR] {e}")
        return "Erro interno no servidor.", 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Rodando servidor Flask na porta {port}")
    app.run(host='0.0.0.0', port=port)
