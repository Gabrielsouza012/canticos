from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

# Pasta temporária para salvar vídeos
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_video(url):
    unique_filename = str(uuid.uuid4())  # gera nome único
    output_template = os.path.join(DOWNLOAD_FOLDER, f"{unique_filename}.%(ext)s")
    
    options = {
    'outtmpl': output_template,
    'format': 'mp4',
    'writesubtitles': True,
    'subtitleslangs': ['pt', 'en'],
    'allsubtitles': True,
    'subtitles': 'auto',
    'skip_download': False,
    'cookiesfromfile': 'cookies.txt',  # 👈 ESSA LINHA GARANTE O USO DOS COOKIES
}
    
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_filename = ydl.prepare_filename(info)
        
        # Corrige se o arquivo baixado tiver extensão diferente
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
    
    if not url:
        return "Nenhum link enviado."
    
    video_path = download_video(url)
    
    return send_file(video_path, as_attachment=True)

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

