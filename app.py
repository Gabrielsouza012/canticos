from flask import Flask, render_template, request, send_file
import yt_dlp
from yt_dlp.utils import DownloadError
import os
import re
import uuid
import subprocess

app = Flask(__name__)

# Cria a pasta de downloads se não existir
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_video(url):
    print("▶️ Iniciando download com yt-dlp")
    print("[yt-dlp version]", subprocess.getoutput("yt-dlp --version"))
    print("[ffmpeg version]", subprocess.getoutput("ffmpeg -version"))

    unique_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_FOLDER, f"%(title)s_{unique_id}.%(ext)s")

    options = {
        'outtmpl': output_template,
        'format': 'best',
        'noplaylist': True,
        'logger': yt_dlp.utils.std_logger(),
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        final_path = ydl.prepare_filename(info)
        print("✅ Arquivo baixado com sucesso:", final_path)
        return final_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('video_urls', '').strip()

    print("📥 URL recebida:", url)

    if not url:
        print("❌ Nenhum link foi enviado.")
        return "Nenhum link enviado.", 400

    try:
        video_path = download_video(url)
        print("📁 Enviando arquivo:", video_path)
        return send_file(video_path, as_attachment=True)
    except DownloadError as e:
        print("⚠️ Erro do yt-dlp:", e)
        return "Erro: vídeo indisponível ou inválido.", 400
    except Exception as e:
        print("❌ Erro inesperado:", e)
        return "Erro interno no servidor.", 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Servidor iniciado na porta {port}")
    app.run(host='0.0.0.0', port=port)
