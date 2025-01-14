FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Copiar arquivos do projeto para o contêiner
COPY . /app

# Instalar dependências do Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Comando para iniciar o app
CMD ["gunicorn", "app:app"]