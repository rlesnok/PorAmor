#!/bin/bash

# Adiciona o repositório da Microsoft para o driver ODBC
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Atualiza os pacotes e instala o driver ODBC necessário
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc

# Inicia o aplicativo Flask com Gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT
