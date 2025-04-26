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
        'format': quality,  # 👈 Usa a qualidade que o usuário escolheu
        'writesubtitles': True,
        'subtitleslangs': ['pt', 'en'],
        'allsubtitles': True,
        'subtitles': 'auto',
        'skip_download': False,
        'cookiefile': 'cookies.txt',  # 👈 Usa cookies para pegar vídeos privados
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
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['video_urls'].strip()
    quality = request.form.get('quality', 'best')  # 👈 pega a escolha de resolução do formulário
    
    if not url:
        return "Nenhum link enviado."
    
    video_path = download_video(url, quality)
    
    return send_file(video_path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # 👈 pega a porta do Render automaticamente
    app.run(host='0.0.0.0', port=port)         # 👈 deixa público para a internet
