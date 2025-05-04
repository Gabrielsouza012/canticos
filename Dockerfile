# Usa uma imagem oficial do Python como base
FROM python:3.11-slim

# Instala o ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Cria diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Comando para rodar o app
CMD ["python", "app.py"]
