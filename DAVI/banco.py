import sqlite3

def create_database():
    try:
        # Conecte-se ao banco de dados (se não existir, será criado)
        conn = sqlite3.connect('watched_list.db')

        # Crie uma tabela para armazenar as séries/filmes assistidos
        conn.execute('''CREATE TABLE IF NOT EXISTS watched (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        last_episode INTEGER,
                        cover_image BLOB
                        )''')

        # Feche a conexão com o banco de dados
        conn.close()

        print("Banco de dados criado com sucesso!")
    except Exception as e:
        print("Erro ao criar o banco de dados:", e)

# Chamando a função para criar o banco de dados
create_database()
