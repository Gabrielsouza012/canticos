from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import re
import uuid

app = Flask(__name__)

# Pasta temporária para salvar vídeos
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def sanitize_filename(name):
    # Remove caracteres inválidos para nome de arquivos
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_video(url):
    # Primeiro baixa as informações para pegar o título
    ydl_opts_info = {}
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(url, download=False)

    title = sanitize_filename(info.get('title', 'video'))

    # Adicionando um identificador único ao nome do arquivo
    unique_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_FOLDER, f"{title}_{unique_id}.%(ext)s")
    
    options = {
        'outtmpl': output_template,
        'format': 'bv*+ba',  # Melhor vídeo e áudio combinados
        'writesubtitles': True,
        'subtitleslangs': ['pt', 'en'],
        'allsubtitles': True,
        'subtitles': 'auto',
        'skip_download': False,
        'cookiefile': 'cookies.txt',  # Usar cookies para YouTube
        'audioquality': 0,  # Melhor qualidade de áudio
        'noplaylist': True,  # Não processar playlists, apenas um vídeo por vez
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_filename = ydl.prepare_filename(info)

    # Retorna o caminho correto do arquivo baixado (não alterando a extensão para .mp4)
    return downloaded_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['video_urls'].strip()
    
    if not url:
        return "Nenhum link enviado."
    
    video_path = download_video(url)
    
    return send_file(video_path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
