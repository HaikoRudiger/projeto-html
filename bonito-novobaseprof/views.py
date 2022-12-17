from flask import render_template, request, redirect, session, flash, url_for
from main import app, db
from models import Pessoas, Usuario


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
    
    pessoa = Pessoas.query.filter_by(nome=nome).firts()
    
    if pessoa:
        flash('People ja existe')
        return redirect(url_for('index'))
    
    nova_pessoa = Pessoas(nome=nome, idade=idade, altura=altura)
    
    db.session.add(nova_pessoa)
    
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proximo = url_for('editar')))
    
    pessoa = Pessoas.query.filter_by(id=id).firts()
    return render_template('editar.html', titulo = 'Editar Jogo', pessoa=pessoa)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    
        

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