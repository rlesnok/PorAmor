import pyodbc  # Biblioteca para conexão com o SQL Server

# Configuração de conexão
SERVER = 'localhost\\SQLEXPRESS'  # Nome do servidor
DATABASE = 'PorAmor'  # Nome do banco de dados
DRIVER = 'ODBC Driver 17 for SQL Server'  # Driver ODBC
TRUSTED_CONNECTION = 'yes'  # Usando autenticação do Windows

try:
    # Conecta ao banco de dados
    conn = pyodbc.connect(
        f'DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection={TRUSTED_CONNECTION};'
    )
    print("Conexão bem-sucedida!")  # Mensagem de sucesso
    # Testando uma consulta simples
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM dbo.atividades;")
    row = cursor.fetchone()
    if row:
        print("Conexão testada com sucesso. Exemplo de registro:", row)
    else:
        print("Conexão bem-sucedida, mas a tabela está vazia.")
    conn.close()  # Fecha a conexão
except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)