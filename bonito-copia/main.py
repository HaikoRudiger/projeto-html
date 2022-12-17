from flask import Flask, render_template, request, redirect, session, flash, url_for
from models.pessoa import Pessoa
from models.usuario import Usuario


from flask_sqlalchemy import SQLAlchemy


#----------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = 'moredevs'

# string de conexão
app.config['SQLALCHEMY_DATABASE_URI'] = '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = 'postgresql',
    usuario = 'html', 
    senha = '123456',
    servidor = 'localhost:5435',
    database = "postgres"    
)


#----------------------------------------------------------------------

db = SQLAlchemy(app)

class Pessoas(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    altura = db.Column(db.String(5), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.name
    
class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.nickname
    

lista = Pessoas.query.order_by(Pessoas.id)

@app.route('/')
def login():  
    proximo = request.args.get('proximo')  
    return render_template('login.html', titulo = 'Login Usuario', proximo=proximo, pessoas=lista)



@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        
        return redirect('/login')
   
    return render_template('novo.html', titulo = 'Cadastro Pessoa')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    idade = request.form['idade']
    altura = request.form['altura']
    
    pessoa = Pessoa(nome, idade, altura)
    
    lista.append(pessoa)
    
    return redirect(url_for('inicio'))

@app.route('/listar')
def inicio():
    lista = Pessoas.query.order_by(Pessoas.id)
     
    return render_template('index.html', titulo = 'Lista Pessoa', pessoas = lista)


@app.route('/autenticar', methods =['POST',])
def autenticar():
    usuario = Usuario.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        
        if request.form['senha'] == usuario.senha:
            
            session['usuario_logado'] = usuario.nickname
            
            flash(usuario.nickname + ' logado com sucesso')
            
            proxima_pagina = request.form['proximo']

            return redirect(proxima_pagina)

    else:
        flash('Usuario ou senha invalidos')
        return redirect(url_for('login'))
        
@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado')
    return redirect(url_for('login'))

app.run(debug=True)