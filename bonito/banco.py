import psycopg2 

print("Testando...")

try:
    conn = psycopg2.connect( host = "localhost", port = "5435", database = "postgres", user = "html", password = "123456")
    print("Conectado ;)")
    
except Exception:
    print("Não deu boa :(")

if conn is not None:
    
    print("A sua conexão está boa")
    
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE  pessoas (id serial, nome VARCHAR(15)NOT NULL, idade INT NOT NULL, altura varchar(15) NOT NULL, PRIMARY KEY(id));')
    print('Sua tabela jogos foi criada!')

    cursor.execute('CREATE TABLE usuarios  (nome VARCHAR(15) NOT NULL, nickname VARCHAR(30)NOT NULL, senha VARCHAR(30)NOT NULL,  PRIMARY KEY(nickname) );')
    print('Sua tabela usuario foi criada!')

    conn.commit()
    cursor.close()
    conn.close()
    