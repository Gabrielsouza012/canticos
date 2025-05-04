#!/usr/bin/env bash

# Atualiza pacotes e instala ffmpeg
apt-get update && apt-get install -y ffmpeg

# Instala dependências Python
pip install -r requirements.txt
