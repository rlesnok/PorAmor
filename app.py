from flask import Flask, render_template, request, redirect, url_for  # Importações necessárias do Flask
import pyodbc  # Biblioteca para conectar ao SQL Server

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Configura a conexão com o banco de dados SQL Server
def get_db_connection():
    # Substitua as configurações abaixo pelas suas informações do servidor
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'  # Nome do servidor
        'DATABASE=PorAmor;'             # Nome do banco de dados
        'Trusted_Connection=yes;'       # Usa autenticação do Windows
    )
    return conn

# Rota inicial (página de boas-vindas)
@app.route('/')
def home():
    return render_template('home.html')  # Renderiza a nova página inicial

# Rota para adicionar atividades (com suporte a GET e POST)
@app.route('/add_atividade', methods=['GET', 'POST'])
def add_atividade():
    if request.method == 'POST':  # Quando o formulário é enviado
        nome = request.form['nome']  # Obtém o nome da atividade do formulário
        dia = request.form['dia']  # Obtém o dia da atividade
        turno = request.form['turno']  # Obtém o turno da atividade
        vagas_totais = request.form['vagas_totais']  # Obtém o número total de vagas

        # Conecta ao banco de dados e insere a atividade
        conn = get_db_connection()
        conn.execute(
            '''
            INSERT INTO atividades (nome, dia, turno, vagas_totais, vagas_ocupadas)
            VALUES (?, ?, ?, ?, 0)
            ''',
            (nome, dia, turno, vagas_totais)
        )
        conn.commit()  # Salva as alterações no banco de dados
        conn.close()  # Fecha a conexão
        return redirect('/')  # Redireciona para a página inicial após salvar
    return render_template('add_atividade.html')  # Exibe o formulário HTML

# Rota para listar todas as atividades cadastradas
@app.route('/atividades')
def listar_atividades():
    conn = get_db_connection()  # Conecta ao banco de dados
    atividades = conn.execute('SELECT * FROM atividades').fetchall()  # Consulta todas as atividades
    conn.close()  # Fecha a conexão
    return render_template('listar_atividades.html', atividades=atividades)  # Renderiza o template HTML

# Nova rota para inscrever voluntários em uma atividade
@app.route('/inscrever/<int:atividade_id>', methods=['GET', 'POST'])
def inscrever_voluntario(atividade_id):
    conn = get_db_connection()
    atividade = conn.execute('SELECT * FROM atividades WHERE id = ?', (atividade_id,)).fetchone()
    if not atividade:
        conn.close()
        return "Atividade não encontrada!", 404

    if request.method == 'POST':  # Se o formulário for enviado
        nome_voluntario = request.form['nome_voluntario']
        contato_voluntario = request.form['contato_voluntario']

        # Insere o voluntário na tabela de inscrições
        conn.execute(
            '''
            INSERT INTO inscricoes (atividade_id, nome_voluntario, contato_voluntario)
            VALUES (?, ?, ?)
            ''',
            (atividade_id, nome_voluntario, contato_voluntario)
        )
        # Atualiza o número de vagas ocupadas
        conn.execute(
            '''
            UPDATE atividades
            SET vagas_ocupadas = vagas_ocupadas + 1
            WHERE id = ?
            ''',
            (atividade_id,)
        )
        conn.commit()
        conn.close()
        return redirect('/atividades')  # Redireciona para a lista de atividades após inscrição
    conn.close()
    return render_template('inscrever.html', atividade=atividade)  # Exibe o formulário de inscrição

# Rota para listar voluntários inscritos em uma atividade
@app.route('/voluntarios/<int:atividade_id>')
def listar_voluntarios(atividade_id):
    conn = get_db_connection()
    atividade = conn.execute('SELECT * FROM atividades WHERE id = ?', (atividade_id,)).fetchone()
    if not atividade:
        conn.close()
        return "Atividade não encontrada!", 404

    # Consulta os voluntários inscritos na atividade
    voluntarios = conn.execute(
        '''
        SELECT id, nome_voluntario, contato_voluntario
        FROM inscricoes
        WHERE atividade_id = ?
        ''',
        (atividade_id,)
    ).fetchall()
    conn.close()

    # Renderiza o template para listar os voluntários
    return render_template('listar_voluntarios.html', atividade=atividade, voluntarios=voluntarios)

# Rota para remover uma inscrição
@app.route('/remover_inscricao/<int:inscricao_id>/<int:atividade_id>', methods=['POST'])
def remover_inscricao(inscricao_id, atividade_id):
    conn = get_db_connection()
    # Remove a inscrição
    conn.execute('DELETE FROM inscricoes WHERE id = ?', (inscricao_id,))
    # Atualiza as vagas ocupadas
    conn.execute(
        '''
        UPDATE atividades
        SET vagas_ocupadas = vagas_ocupadas - 1
        WHERE id = ?
        ''',
        (atividade_id,)
    )
    conn.commit()
    conn.close()
    return redirect(f'/voluntarios/{atividade_id}')  # Redireciona para a lista de voluntários

# Inicia o servidor Flask
if __name__ == '__main__':
    print("Iniciando o servidor Flask...")
    # Exibe as rotas registradas no Flask (temporário, para depuração)
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:20s} {rule.methods} {rule}")
    # Roda o servidor no modo de depuração
    app.run(debug=True)