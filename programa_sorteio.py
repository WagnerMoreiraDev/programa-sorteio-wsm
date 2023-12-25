from flask import Flask, render_template
import random

app = Flask(__name__)

def ler_nomes_do_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        nomes = [linha.strip() for linha in file]
    return nomes

def realizar_sorteio(pessoas, quantidade_sorteio):
    if quantidade_sorteio > len(pessoas):
        raise ValueError("A quantidade de pessoas para o sorteio é maior do que o número total de pessoas.")
    random.shuffle(pessoas)
    resultado_sorteio = pessoas[:quantidade_sorteio]
    return resultado_sorteio

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sorteio')
def sorteio():
    nome_arquivo = 'nomes_pessoas.txt'
    nomes_pessoas = ler_nomes_do_arquivo(nome_arquivo)
    quantidade_sorteio = 5
    resultado = realizar_sorteio(nomes_pessoas, quantidade_sorteio)
    return render_template('sorteio.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
