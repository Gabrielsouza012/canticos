FROM python:3.11-slim

# Instala ffmpeg e limpa cache
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
