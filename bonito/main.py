from flask import Flask, render_template, request, redirect, session, flash, url_for
from models.pessoa import Pessoa
from models.usuario import Usuario


from flask_sqlalchemy import SQLAlchemy


#----------------------------------------------------------------------


#----------------------------------------------------------------------

pessoa1 = Pessoa('haiko', '16', '1:50')
pessoa2 = Pessoa('j', '6', '1:70')
pessoa3 = Pessoa('abacate', '10', '2:50')

lista = [pessoa1, pessoa2, pessoa3]

usuario1 = Usuario('admin', 'admin', '1234')
usuario2 = Usuario('boa', 'mal', '4321')
usuario3 = Usuario('php', 'cruzes', '90')

usuarios = {usuario1.nickname: usuario1, usuario2.nickname: usuario2, usuario3.nickname: usuario3}

app = Flask(__name__)
app.secret_key = 'moredevs'




@app.route('/')
def login():  
    proximo = request.args.get('proximo')  
    return render_template('login.html', titulo = 'Login Usuario', proximo=proximo)

# def inicio():
#     return render_template('index.html', titulo = 'Lista Pessoa', pessoas = lista)


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
    
    abacate = Pessoa(nome, idade, altura)
    
    lista.append(abacate)
    
    return redirect(url_for('inicio'))

@app.route('/listar')
def inicio():
     return render_template('index.html', titulo = 'Lista Pessoa', pessoas = lista)

# def login():  
#     # proximo = request.args.get('proximo')  
#     # return render_template('login.html', titulo = 'Login Usuario', proximo=proximo)

@app.route('/autenticar', methods =['POST',])
def autenticar():
    
    if request.form['usuario'] in usuarios:
        
        usuario = usuarios[request.form['usuario']]
        
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            
            flash(usuario.nickname + ' Deu Boa')
            proxima_pagina = request.form['proximo']
            return redirect(proxima_pagina)
        
        else:
            flash('Usuario ou senha invalidos')
            return redirect(url_for('login'))
        
    else:
        flash('Usuario ou senha invalidos')
        return redirect(url_for('login'))
        
@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado')
    return redirect(url_for('login'))

app.run(debug=True)