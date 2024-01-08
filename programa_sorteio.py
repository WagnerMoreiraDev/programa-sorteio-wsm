from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random

app = Flask(__name__)

# Função para criar a tabela no banco de dados
def criar_tabela():
    conn = sqlite3.connect('nomes_pessoas.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Função para ler os nomes do banco de dados
def ler_nomes_do_banco():
    conn = sqlite3.connect('nomes_pessoas.db')
    cursor = conn.cursor()

    cursor.execute('SELECT nome FROM pessoas')
    nomes = [row[0] for row in cursor.fetchall()]

    conn.close()

    return nomes

# Rota principal - exibe a página inicial
@app.route('/')
def index():
    nomes_pessoas = ler_nomes_do_banco()
    return render_template('index.html', nomes_pessoas=nomes_pessoas)

# Rota para exibir o formulário de adição de nome
@app.route('/adicionar', methods=['GET'])
def exibir_formulario_adicionar():
    return render_template('adicionar.html')

# Rota para processar a adição de nome
@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']

    # Adiciona o nome ao banco de dados se não for vazio
    if nome:
        adicionar_nome_ao_banco(nome)

    # Redireciona para a página inicial
    return redirect(url_for('index'))

# Rota para exibir o resultado do sorteio
@app.route('/sorteio')
def sorteio():
    nomes_pessoas = ler_nomes_do_banco()
    quantidade_sorteio = 6

    # Verifica se há pessoas suficientes para o sorteio
    if len(nomes_pessoas) < quantidade_sorteio:
        return "Não há pessoas suficientes para realizar o sorteio."

    try:
        # Realiza o sorteio
        resultado = realizar_sorteio(nomes_pessoas, quantidade_sorteio)
    except ValueError as e:
        return str(e)

    return render_template('sorteio.html', resultado=resultado)

# Função para realizar o sorteio
def realizar_sorteio(pessoas, quantidade_sorteio):
    if quantidade_sorteio > len(pessoas):
        raise ValueError("A quantidade de pessoas para o sorteio é maior do que o número total de pessoas.")

    return random.sample(pessoas, quantidade_sorteio)

# Função para adicionar um nome ao banco de dados
def adicionar_nome_ao_banco(nome):
    conn = sqlite3.connect('nomes_pessoas.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO pessoas (nome) VALUES (?)', (nome,))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Inicializa o banco de dados ao iniciar o aplicativo
    criar_tabela()

    # Roda o aplicativo Flask
    app.run(debug=True)
