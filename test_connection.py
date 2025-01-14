import pyodbc

conn_str = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=PorAmor;Trusted_Connection=yes;'

try:
    conn = pyodbc.connect(conn_str)
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print("Erro na conexão:", e)