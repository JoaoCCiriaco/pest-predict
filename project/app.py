from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def conectar_banco():
    conexao = sqlite3.connect("database.db")
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela_inspecoes():

    conexao = conectar_banco()

    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS inspecoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caixa_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            consumo TEXT NOT NULL,
            observacao TEXT,
            FOREIGN KEY (caixa_id) REFERENCES caixas(id)
        )
        """
    )

    conexao.commit()
    conexao.close()


@app.route("/")
def index():

    conexao = conectar_banco()

    clientes = conexao.execute(
        "SELECT * FROM clientes"
    ).fetchall()

    caixas = conexao.execute(
        "SELECT * FROM caixas"
    ).fetchall()

    conexao.close()

    return render_template(
        "index.html",
        clientes=clientes,
        caixas=caixas
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
        "SELECT * FROM clientes"
    ).fetchall()

    conexao.close()

    return render_template(
        "lista_clientes.html",
        clientes=clientes
    )


@app.route("/excluir-cliente/<int:id>")
def excluir_cliente(id):

    conexao = conectar_banco()

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
        "SELECT * FROM clientes"
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
        "SELECT * FROM clientes"
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

    conexao.execute(
        "DELETE FROM inspecoes WHERE caixa_id = ?",
        (id,)
    )

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
        observacao = request.form["observacao"]

        conexao.execute(
            """
            INSERT INTO inspecoes
            (caixa_id, data, consumo, observacao)
            VALUES (?, ?, ?, ?)
            """,
            (caixa_id, data, consumo, observacao)
        )

        conexao.commit()
        conexao.close()

        return redirect(f"/historico-caixa/{caixa_id}")

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
        observacao = request.form["observacao"]

        conexao.execute(
            """
            INSERT INTO inspecoes
            (caixa_id, data, consumo, observacao)
            VALUES (?, ?, ?, ?)
            """,
            (caixa_id, data, consumo, observacao)
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


if __name__ == "__main__":

    criar_tabela_inspecoes()

    app.run(debug=True)
