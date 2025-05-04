from flask import Flask, render_template, request, send_file
import yt_dlp
from yt_dlp.utils import DownloadError
import os
import re
import uuid

app = Flask(__name__)

# Pasta para salvar os vídeos baixados
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def sanitize_filename(name):
    # Remove caracteres inválidos para nomes de arquivos
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_video(url):
    # Primeiro baixa as informações para obter o título
    ydl_opts_info = {}
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(url, download=False)

    title = sanitize_filename(info.get('title', 'video'))

    # Nome do arquivo com identificador único
    unique_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_FOLDER, f"{title}_{unique_id}.%(ext)s")

    options = {
        'outtmpl': output_template,
        'format': 'bv*+ba',  # Melhor vídeo + áudio
        'writesubtitles': True,
        'subtitleslangs': ['pt', 'en'],
        'allsubtitles': True,
        'subtitles': 'auto',
        'skip_download': False,
        # Remova ou mantenha se você realmente tiver um cookies.txt válido:
        # 'cookiefile': 'cookies.txt',
        'audioquality': 0,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_filename = ydl.prepare_filename(info)

    return downloaded_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('video_urls', '').strip()

    if not url:
        return "Nenhum link enviado.", 400

    # Verificação simples de URL do YouTube
    if not re.match(r'^https:\/\/(www\.)?youtube\.com\/watch\?v=', url):
        return "Erro: URL inválida do YouTube.", 400

    try:
        video_path = download_video(url)
        response = send_file(video_path, as_attachment=True)

        # (Opcional) Apaga o arquivo após envio
        # os.remove(video_path)

        return response
    except DownloadError as e:
        print(f"[yt_dlp ERROR] {e}")
        return "Erro: O vídeo está indisponível ou não pode ser baixado.", 400
    except Exception as e:
        print(f"[Unhandled ERROR] {e}")
        return "Erro interno no servidor.", 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
