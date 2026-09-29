import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configuração da aplicação
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configuração da sessão
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ligação ao banco de dados SQLite
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Garante que as respostas não fiquem em cache"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Mostrar portfólio de ações"""
    user_id = session["user_id"]
    rows = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        user_id
    )
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    grand_total = user_cash
    stocks = []

    for row in rows:
        stock_info = lookup(row["symbol"])
        price = stock_info["price"]
        total_value = price * row["total_shares"]
        grand_total += total_value

        stocks.append({
            "symbol": row["symbol"],
            "shares": row["total_shares"],
            "price": price,
            "total": total_value
        })

    return render_template("index.html", stocks=stocks, cash=user_cash, total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Comprar ações"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("tem de indicar o símbolo", 400)

        stock = lookup(symbol.upper())
        if stock is None:
            return apology("símbolo inválido", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("a quantidade deve ser positiva", 400)
        except (ValueError, TypeError):
            return apology("a quantidade deve ser um número", 400)

        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        total_cost = shares * stock["price"]

        if user_cash < total_cost:
            return apology("saldo insuficiente", 400)

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            user_id, stock["symbol"], shares, stock["price"]
        )

        flash("Compra efetuada com sucesso!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Histórico de transações"""
    user_id = session["user_id"]
    transactions = db.execute(
        "SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = ? ORDER BY transacted DESC",
        user_id
    )
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Iniciar sessão"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("tem de indicar o utilizador", 400)
        elif not password:
            return apology("tem de indicar a palavra-passe", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("utilizador ou palavra-passe incorretos", 400)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Encerrar sessão"""
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Consultar cotação de ação"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("tem de indicar o símbolo", 400)

        stock = lookup(symbol.upper())
        if stock is None:
            return apology("símbolo inválido", 400)

        return render_template("quoted.html", stock=stock)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registar utilizador"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("tem de indicar um nome de utilizador", 400)
        elif not password:
            return apology("tem de indicar uma palavra-passe", 400)
        elif not confirmation:
            return apology("tem de confirmar a palavra-passe", 400)
        elif password != confirmation:
            return apology("as palavras-passe não coincidem", 400)

        hash_password = generate_password_hash(password)

        try:
            new_id = db.execute(
                "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
                username, hash_password, 10000.00
            )
        except Exception:
            return apology("nome de utilizador já existe", 400)

        session["user_id"] = new_id
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Vender ações"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("tem de selecionar uma ação", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("a quantidade deve ser positiva", 400)
        except (ValueError, TypeError):
            return apology("a quantidade deve ser um número", 400)

        user_shares = db.execute(
            "SELECT SUM(shares) as total FROM transactions WHERE user_id = ? AND symbol = ?",
            user_id, symbol
        )

        if not user_shares or user_shares[0]["total"] is None or user_shares[0]["total"] < shares:
            return apology("não tem ações suficientes", 400)

        stock = lookup(symbol)
        if stock is None:
            return apology("símbolo inválido", 400)

        total_income = shares * stock["price"]

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_income, user_id)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            user_id, symbol, -shares, stock["price"]
        )

        flash("Venda efetuada com sucesso!")
        return redirect("/")

    else:
        symbols = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
            user_id
        )
        return render_template("sell.html", symbols=symbols)
