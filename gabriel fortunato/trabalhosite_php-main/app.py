from flask import Flask, redirect, render_template, request, url_for,flash,session
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
    dados.execute('CREATE TABLE usuarios (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255),email VARCHAR(255),senha VARCHAR(255),perfil VARCHAR(255));')

    
    sql.commit()
    sql.close()





app = Flask(__name__)
app.config['SECRET_KEY']='TESTE'
@app.route('/')


def index():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    
    
    return render_template('index.html')
    



@app.route('/dados')
def dados():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    sql = conecta_banco()
    dados = sql.cursor()
    
    dados.execute('SELECT * FROM usuarios')
    table_data = dados.fetchall()
    print(table_data)
    return render_template('dados.html', table_data=table_data)


@app.route('/cadastro', methods=["POST","GET"])

def cadastro():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    perfil = request.form.get('perfil')
    print(perfil)
    if nome == None or nome == '':
        print('O nome esta em branco')
        return render_template('cadastro.html', error='Método HTTP inválido.')
    
    if email == None or email == '':
        print('email esta em branco')
        return render_template('cadastro.html', error='Método HTTP inválido.')
    
    if senha == None or senha == '':
        print('A senha esta em branco')

        return render_template('cadastro.html', error='Método HTTP inválido.')
    print(nome,email,senha)
    
    sql = conecta_banco()
    
    dados = sql.cursor()
    dados.execute('INSERT INTO usuarios (nome,email,senha,perfil) VALUES (%s,%s, %s, %s)', (nome,email, senha,perfil))

    sql.commit()
    sql.close()
    
    return render_template('cadastro.html')


@app.route('/excluir_usuario/<id>', methods=['GET', 'POST'])
def excluir_usuario(id):
    
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
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

   
   
   
   


@app.route('/pagina_login',methods=['POST','GET'])
def pagina_login():
     # Limpa os dados da sessão
     session.clear()
      # Limpa o cookie do ID do usuário
     session.pop('usuario_id', None)
     # Renderiza o template 'login.html' e retorna a página HTML gerada.
     return render_template("login.html")


@app.route('/validalogin', methods=['POST', 'GET'])

def login():

    email = request.form.get('email')
    senha = request.form.get('senha')
    print(email,senha)
    # Validar as credenciais
    sql = conecta_banco() 
    dados = sql.cursor()
    dados.execute("""
                SELECT *
                FROM usuarios
                WHERE email = %s AND senha = %s;
            """, (email, senha,))
    usuario = dados.fetchone()
    dados.close()
    sql.close()

    if usuario:
        # Login bem-sucedido
        session.clear()
        session['usuario_id'] = usuario[0]
        session['nome']=usuario[1]

        session['perfil']=usuario[4]
        return redirect(url_for('index'))
    else:
        # Login inválido
        
        return redirect(url_for('index'))





@app.route('/edit_user/<id>', methods=['POST', 'GET'])

def edit_user(id):
    
 
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if nome == None or nome == '':
            print('O nome esta em branco')
            return render_template('cadastro.html', error='Método HTTP inválido.')
        
        if email == None or email == '':
            print('email esta em branco')
            return render_template('cadastro.html', error='Método HTTP inválido.')
        
        if senha == None or senha == '':
            print('A senha esta em branco')

            return render_template('cadastro.html', error='Método HTTP inválido.')
        
        
        sql = conecta_banco()
        
        dados = sql.cursor()
        print(nome,email,senha,id)
        dados.execute('UPDATE usuarios SET nome = %s, email = %s, senha=%s WHERE id = %s;',(nome,email,senha,id))

        sql.commit()
        sql.close()
        return redirect(url_for('dados'))
        
    
    return render_template('editar_usuario.html', id=id)






if __name__ == '__main__':
    app.run(debug=True , use_reloader=True)
