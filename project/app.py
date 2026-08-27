from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def conectar_banco():
    conexao = sqlite3.connect("database.db")
    conexao.row_factory = sqlite3.Row
    return conexao


@app.route("/")
def index():

    conexao = conectar_banco()

    clientes = conexao.execute(
        "SELECT * FROM clientes"
    ).fetchall()

    conexao.close()

    return render_template(
        "index.html",
        clientes=clientes
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


if __name__ == "__main__":
    app.run(debug=True)
