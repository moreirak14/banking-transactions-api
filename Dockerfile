FROM python:3.12-slim-bullseye

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando os arquivos do contexto para o diretório de trabalho
COPY . /app/

# Usar /bin/bash em vez de /bin/sh
SHELL ["/bin/bash", "-c"]

# Atualizando pacotes, instalando dependências, atualizando pip e instalando o Poetry
RUN apt-get update && \
    pip install --upgrade pip && \
    pip install poetry==1.8.4 && \
    poetry install --no-root

# Expondo a porta
EXPOSE 8080