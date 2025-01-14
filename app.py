from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import os  # Importar os para usar variáveis de ambiente

app = Flask(__name__)

# Configura a conexão com o banco de dados usando variáveis de ambiente
def get_db_connection():
    server = os.getenv('DB_SERVER', 'localhost\\SQLEXPRESS')
    database = os.getenv('DB_NAME', 'PorAmor')
    username = os.getenv('DB_USERNAME', '')
    password = os.getenv('DB_PASSWORD', '')
    
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )
    return conn

# As demais rotas permanecem iguais...

if __name__ == '__main__':
    app.run(debug=True)