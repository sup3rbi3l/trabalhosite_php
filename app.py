from flask import Flask, redirect, render_template, request, url_for
import mysql.connector
from hashlib import scrypt
import warnings

def conecta_banco():
    sql = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database= 'dados'
    )
    return sql


sql = mysql.connector.connect(
  host='127.0.0.1',
  user='root',
  password=''
)

dados = sql.cursor()
dados.execute('SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "dados";')
resultado = dados.fetchone()[0]

if resultado > 0 :
    sql.close()
    sql = conecta_banco()
    print('O banco foi encontrado!!!')

else:
    
    dados.execute('CREATE DATABASE dados;')
    sql.commit()
    
    sql = conecta_banco()

    dados = sql.cursor()
    dados.execute('CREATE TABLE usuarios (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), idade VARCHAR(255),cidade VARCHAR(255));')

    
    sql.commit()
    sql.close()





app = Flask(__name__)

@app.route('/')
def index():
    # Dados da tabela (pode ser uma lista de listas)
    

    return render_template('index.html')


@app.route('/dados')
def dados():
    
    sql = conecta_banco()
    dados = sql.cursor()
    
    dados.execute('SELECT * FROM usuarios')
    table_data = dados.fetchall()
    print(table_data)
    return render_template('dados.html', table_data=table_data)


@app.route('/cadastro', methods=["POST","GET"])

def cadastro():
    
    
    nome = request.form.get('nome')
    idade = request.form.get('idade')
    cidade = request.form.get('cidade')
    
    if nome == None or nome == '':
        print('O nome esta em branco')
        return render_template('cadastro.html', error='Método HTTP inválido.')
    
    if idade == None or idade == '':
        print('A idade esta em branco')
        return render_template('cadastro.html', error='Método HTTP inválido.')
    
    if cidade == None or cidade == '':
        print('A cidade esta em branco')

        return render_template('cadastro.html', error='Método HTTP inválido.')
    print(nome,idade,cidade)
    
    sql = conecta_banco()
    
    dados = sql.cursor()
    dados.execute('INSERT INTO usuarios (nome, idade,cidade) VALUES (%s, %s, %s)', (nome, idade, cidade))

    sql.commit()
    sql.close()
    
    return render_template('cadastro.html')


@app.route('/excluir_usuario/<id>', methods=['GET', 'POST'])
def excluir_usuario(id):
    # Validar o ID
    print(id)
    if not id.isdigit():
        return render_template('excluir-usuario.html', error='ID inválido')
    # Executando a exclusão

    sql = conecta_banco()

    dados = sql.cursor()
    dados.execute("""
        DELETE FROM usuarios
        WHERE id = %s;
    """, (id,))
    dados.close()
    sql.commit()

    return redirect(url_for('dados'))

   


if __name__ == '__main__':
    app.run(debug=True , use_reloader=True)
