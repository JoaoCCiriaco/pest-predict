import sqlite3


conexao = sqlite3.connect("database.db")


conexao.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    email TEXT
)
""")


conexao.execute("""
CREATE TABLE IF NOT EXISTS caixas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    local TEXT NOT NULL,
    status TEXT DEFAULT 'Ativa',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
)
""")


conexao.commit()

conexao.close()

print("Banco de dados configurado com sucesso!")
