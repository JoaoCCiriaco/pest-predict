from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)


def conectar_banco():
    conexao = sqlite3.connect("database.db")
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela_inspecoes():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS inspecoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caixa_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            consumo TEXT NOT NULL,
            observacao TEXT,
            tecnico TEXT,
            horario TEXT,
            FOREIGN KEY (caixa_id) REFERENCES caixas(id)
        )
    """)

    colunas = conexao.execute(
        "PRAGMA table_info(inspecoes)"
    ).fetchall()

    nomes_colunas = [coluna["name"] for coluna in colunas]

    if "tecnico" not in nomes_colunas:
        conexao.execute(
            "ALTER TABLE inspecoes ADD COLUMN tecnico TEXT"
        )

    if "horario" not in nomes_colunas:
        conexao.execute(
            "ALTER TABLE inspecoes ADD COLUMN horario TEXT"
        )

    conexao.commit()
    conexao.close()


@app.route("/")
def index():
    conexao = conectar_banco()

    clientes = conexao.execute(
        "SELECT * FROM clientes ORDER BY id"
    ).fetchall()

    caixas = conexao.execute(
        """
        SELECT
            caixas.id,
            caixas.cliente_id,
            caixas.local,
            caixas.status,
            clientes.nome AS cliente_nome
        FROM caixas
        JOIN clientes
            ON caixas.cliente_id = clientes.id
        ORDER BY caixas.id
        """
    ).fetchall()

    # Conta somente inspeções de caixas que ainda existem
    total_inspecoes = conexao.execute(
        """
        SELECT COUNT(*) AS total
        FROM inspecoes
        JOIN caixas
            ON inspecoes.caixa_id = caixas.id
        """
    ).fetchone()["total"]

    # Conta somente inspeções válidas com consumo
    inspecoes_consumo = conexao.execute(
        """
        SELECT COUNT(*) AS total
        FROM inspecoes
        JOIN caixas
            ON inspecoes.caixa_id = caixas.id
        WHERE inspecoes.consumo = 'Sim'
        """
    ).fetchone()["total"]

    # Conta somente inspeções válidas sem consumo
    inspecoes_sem_consumo = conexao.execute(
        """
        SELECT COUNT(*) AS total
        FROM inspecoes
        JOIN caixas
            ON inspecoes.caixa_id = caixas.id
        WHERE inspecoes.consumo = 'Não'
        """
    ).fetchone()["total"]

    # Busca a última inspeção de uma caixa que ainda existe
    ultima_inspecao = conexao.execute(
        """
        SELECT
            inspecoes.id,
            inspecoes.caixa_id,
            inspecoes.data,
            inspecoes.consumo,
            inspecoes.observacao,
            inspecoes.tecnico,
            inspecoes.horario,
            caixas.local,
            clientes.nome AS cliente_nome
        FROM inspecoes
        JOIN caixas
            ON inspecoes.caixa_id = caixas.id
        JOIN clientes
            ON caixas.cliente_id = clientes.id
        ORDER BY inspecoes.data DESC, inspecoes.id DESC
        LIMIT 1
        """
    ).fetchone()

    conexao.close()

    return render_template(
        "index.html",
        clientes=clientes,
        caixas=caixas,
        total_inspecoes=total_inspecoes,
        inspecoes_consumo=inspecoes_consumo,
        inspecoes_sem_consumo=inspecoes_sem_consumo,
        ultima_inspecao=ultima_inspecao
    )


@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        email = request.form["email"]

        conexao = conectar_banco()

        conexao.execute(
            """
            INSERT INTO clientes (nome, telefone, email)
            VALUES (?, ?, ?)
            """,
            (nome, telefone, email)
        )

        conexao.commit()
        conexao.close()

        return redirect("/lista-clientes")

    return render_template("clientes.html")


@app.route("/lista-clientes")
def lista_clientes():
    conexao = conectar_banco()

    clientes = conexao.execute(
        "SELECT * FROM clientes ORDER BY id"
    ).fetchall()

    conexao.close()

    return render_template(
        "lista_clientes.html",
        clientes=clientes
    )


@app.route("/excluir-cliente/<int:id>")
def excluir_cliente(id):
    conexao = conectar_banco()

    # Remove caixas do cliente e suas inspeções antes de excluir o cliente
    caixas = conexao.execute(
        "SELECT id FROM caixas WHERE cliente_id = ?",
        (id,)
    ).fetchall()

    for caixa in caixas:
        conexao.execute(
            "DELETE FROM inspecoes WHERE caixa_id = ?",
            (caixa["id"],)
        )

    conexao.execute(
        "DELETE FROM caixas WHERE cliente_id = ?",
        (id,)
    )

    conexao.execute(
        "DELETE FROM clientes WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/lista-clientes")


@app.route("/editar-cliente/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    conexao = conectar_banco()

    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        email = request.form["email"]

        conexao.execute(
            """
            UPDATE clientes
            SET nome = ?, telefone = ?, email = ?
            WHERE id = ?
            """,
            (nome, telefone, email, id)
        )

        conexao.commit()
        conexao.close()

        return redirect("/lista-clientes")

    cliente = conexao.execute(
        "SELECT * FROM clientes WHERE id = ?",
        (id,)
    ).fetchone()

    conexao.close()

    if cliente is None:
        return "Cliente não encontrado"

    return render_template(
        "editar_cliente.html",
        cliente=cliente
    )


@app.route("/caixas", methods=["GET", "POST"])
def caixas():
    conexao = conectar_banco()

    if request.method == "POST":
        cliente_id = request.form["cliente_id"]
        local = request.form["local"]
        status = request.form["status"]

        conexao.execute(
            """
            INSERT INTO caixas (cliente_id, local, status)
            VALUES (?, ?, ?)
            """,
            (cliente_id, local, status)
        )

        conexao.commit()
        conexao.close()

        return redirect("/lista-caixas")

    clientes = conexao.execute(
        "SELECT * FROM clientes ORDER BY nome"
    ).fetchall()

    conexao.close()

    return render_template(
        "caixas.html",
        clientes=clientes
    )


@app.route("/lista-caixas")
def lista_caixas():
    conexao = conectar_banco()

    caixas = conexao.execute(
        """
        SELECT
            caixas.id,
            caixas.cliente_id,
            caixas.local,
            caixas.status,
            clientes.nome AS cliente_nome
        FROM caixas
        JOIN clientes
            ON caixas.cliente_id = clientes.id
        ORDER BY caixas.id
        """
    ).fetchall()

    conexao.close()

    return render_template(
        "lista_caixas.html",
        caixas=caixas
    )


@app.route("/editar-caixa/<int:id>", methods=["GET", "POST"])
def editar_caixa(id):
    conexao = conectar_banco()

    caixa = conexao.execute(
        "SELECT * FROM caixas WHERE id = ?",
        (id,)
    ).fetchone()

    if caixa is None:
        conexao.close()
        return "Caixa não encontrada"

    if request.method == "POST":
        cliente_id = request.form["cliente_id"]
        local = request.form["local"]
        status = request.form["status"]

        conexao.execute(
            """
            UPDATE caixas
            SET cliente_id = ?, local = ?, status = ?
            WHERE id = ?
            """,
            (cliente_id, local, status, id)
        )

        conexao.commit()
        conexao.close()

        return redirect("/lista-caixas")

    clientes = conexao.execute(
        "SELECT * FROM clientes ORDER BY nome"
    ).fetchall()

    conexao.close()

    return render_template(
        "editar_caixa.html",
        caixa=caixa,
        clientes=clientes
    )


@app.route("/excluir-caixa/<int:id>")
def excluir_caixa(id):
    conexao = conectar_banco()

    # Primeiro remove as inspeções da caixa
    conexao.execute(
        "DELETE FROM inspecoes WHERE caixa_id = ?",
        (id,)
    )

    # Depois remove a caixa
    conexao.execute(
        "DELETE FROM caixas WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/lista-caixas")


@app.route("/nova-inspecao/<int:caixa_id>", methods=["GET", "POST"])
def nova_inspecao_caixa(caixa_id):
    conexao = conectar_banco()

    caixa = conexao.execute(
        """
        SELECT
            caixas.id,
            caixas.local,
            caixas.status,
            clientes.nome AS cliente_nome
        FROM caixas
        JOIN clientes
            ON caixas.cliente_id = clientes.id
        WHERE caixas.id = ?
        """,
        (caixa_id,)
    ).fetchone()

    if caixa is None:
        conexao.close()
        return "Caixa não encontrada"

    if request.method == "POST":
        data = request.form["data"]
        consumo = request.form["consumo"]
        observacao = request.form.get("observacao", "")
        tecnico = request.form.get("tecnico", "")

        horario = datetime.now().strftime("%H:%M")

        conexao.execute(
            """
            INSERT INTO inspecoes
            (
                caixa_id,
                data,
                consumo,
                observacao,
                tecnico,
                horario
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                caixa_id,
                data,
                consumo,
                observacao,
                tecnico,
                horario
            )
        )

        conexao.commit()
        conexao.close()

        return redirect(
            f"/historico-caixa/{caixa_id}"
        )

    conexao.close()

    return render_template(
        "nova_inspecao_caixa.html",
        caixa=caixa
    )


@app.route("/nova-inspecao", methods=["GET", "POST"])
def nova_inspecao():
    conexao = conectar_banco()

    if request.method == "POST":
        caixa_id = request.form["caixa_id"]
        data = request.form["data"]
        consumo = request.form["consumo"]
        observacao = request.form.get("observacao", "")
        tecnico = request.form.get("tecnico", "")

        horario = datetime.now().strftime("%H:%M")

        conexao.execute(
            """
            INSERT INTO inspecoes
            (
                caixa_id,
                data,
                consumo,
                observacao,
                tecnico,
                horario
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                caixa_id,
                data,
                consumo,
                observacao,
                tecnico,
                horario
            )
        )

        conexao.commit()
        conexao.close()

        return redirect("/lista-caixas")

    caixas = conexao.execute(
        """
        SELECT
            caixas.id,
            caixas.local,
            clientes.nome AS cliente_nome
        FROM caixas
        JOIN clientes
            ON caixas.cliente_id = clientes.id
        ORDER BY caixas.id
        """
    ).fetchall()

    conexao.close()

    return render_template(
        "nova_inspecao.html",
        caixas=caixas
    )


@app.route("/editar-inspecao/<int:id>", methods=["GET", "POST"])
def editar_inspecao(id):
    conexao = conectar_banco()

    inspecao = conexao.execute(
        "SELECT * FROM inspecoes WHERE id = ?",
        (id,)
    ).fetchone()

    if inspecao is None:
        conexao.close()
        return "Inspeção não encontrada"

    if request.method == "POST":
        data = request.form["data"]
        consumo = request.form["consumo"]
        observacao = request.form.get("observacao", "")
        tecnico = request.form.get("tecnico", "")

        conexao.execute(
            """
            UPDATE inspecoes
            SET
                data = ?,
                consumo = ?,
                observacao = ?,
                tecnico = ?
            WHERE id = ?
            """,
            (
                data,
                consumo,
                observacao,
                tecnico,
                id
            )
        )

        conexao.commit()

        caixa_id = inspecao["caixa_id"]

        conexao.close()

        return redirect(
            f"/historico-caixa/{caixa_id}"
        )

    conexao.close()

    return render_template(
        "editar_inspecao.html",
        inspecao=inspecao
    )


@app.route("/excluir-inspecao/<int:id>")
def excluir_inspecao(id):
    conexao = conectar_banco()

    inspecao = conexao.execute(
        "SELECT caixa_id FROM inspecoes WHERE id = ?",
        (id,)
    ).fetchone()

    if inspecao is None:
        conexao.close()
        return "Inspeção não encontrada"

    caixa_id = inspecao["caixa_id"]

    conexao.execute(
        "DELETE FROM inspecoes WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect(
        f"/historico-caixa/{caixa_id}"
    )


@app.route("/historico-caixa/<int:id>")
def historico_caixa(id):
    conexao = conectar_banco()

    caixa = conexao.execute(
        """
        SELECT
            caixas.id,
            caixas.local,
            caixas.status,
            clientes.nome AS cliente_nome
        FROM caixas
        JOIN clientes
            ON caixas.cliente_id = clientes.id
        WHERE caixas.id = ?
        """,
        (id,)
    ).fetchone()

    if caixa is None:
        conexao.close()
        return "Caixa não encontrada"

    inspecoes = conexao.execute(
        """
        SELECT *
        FROM inspecoes
        WHERE caixa_id = ?
        ORDER BY data DESC, id DESC
        """,
        (id,)
    ).fetchall()

    conexao.close()

    return render_template(
        "historico_caixa.html",
        caixa=caixa,
        inspecoes=inspecoes
    )


@app.route("/qr-code-caixa/<int:id>")
def qr_code_caixa(id):
    conexao = conectar_banco()

    caixa = conexao.execute(
        """
        SELECT
            caixas.id,
            caixas.local,
            caixas.status,
            clientes.nome AS cliente_nome
        FROM caixas
        JOIN clientes
            ON caixas.cliente_id = clientes.id
        WHERE caixas.id = ?
        """,
        (id,)
    ).fetchone()

    conexao.close()

    if caixa is None:
        return "Caixa não encontrada"

    return render_template(
        "qr_code_caixa.html",
        caixa=caixa
    )


if __name__ == "__main__":
    criar_tabela_inspecoes()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
