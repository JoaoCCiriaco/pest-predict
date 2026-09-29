import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    try:
        rows = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
            user_id
        )
    except Exception:
        rows = []

    user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    user_cash = user_cash_db[0]["cash"] if user_cash_db else 10000.00

    grand_total = user_cash
    stocks = []

    for row in rows:
        stock_info = lookup(row["symbol"])
        if stock_info:
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
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)

        stock = lookup(symbol.upper())
        if stock is None:
            return apology("invalid symbol", 400)

        try:
            shares_int = int(shares)
            if shares_int <= 0 or str(float(shares)) != str(float(shares_int)):
                return apology("shares must be a positive integer", 400)
        except (ValueError, TypeError):
            return apology("shares must be a positive integer", 400)

        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        total_cost = shares_int * stock["price"]

        if user_cash < total_cost:
            return apology("can't afford", 400)

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            user_id, stock["symbol"], shares_int, stock["price"]
        )

        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    try:
        transactions = db.execute(
            "SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = ? ORDER BY transacted DESC",
            user_id
        )
    except Exception:
        transactions = []

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username", Aqui está o código completo do **`app.py`**, escrito de forma limpa, direta e com todas as rotas e validações necessárias para passar no `check50`.

Substitua todo o conteúdo do arquivo **`app.py`** por este:

```python
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

# Conexão com o banco de dados
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
        if stock_info:
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
            return apology("deve fornecer o símbolo", 400)

        stock = lookup(symbol.upper())
        if stock is None:
            return apology("símbolo inválido", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("quantidade deve ser um número inteiro positivo", 400)
        except (ValueError, TypeError):
            return apology("quantidade deve ser um número inteiro", 400)

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

        flash("Compra realizada com sucesso!")
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
            return apology("deve fornecer o nome de usuário", 400)
        elif not password:
            return apology("deve fornecer a senha", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("usuário ou senha inválidos", 400)

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
            return apology("deve fornecer o símbolo", 400)

        stock = lookup(symbol.upper())
        if stock is None:
            return apology("símbolo inválido", 400)

        return render_template("quoted.html", stock=stock)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registrar novo usuário"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("deve fornecer um nome de usuário", 400)
        elif not password:
            return apology("deve fornecer uma senha", 400)
        elif not confirmation:
            return apology("deve confirmar a senha", 400)
        elif password != confirmation:
            return apology("as senhas não coincidem", 400)

        hash_password = generate_password_hash(password)

        try:
            new_id = db.execute(
                "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
                username, hash_password, 10000.00
            )
        except Exception:
            return apology("nome de usuário já existe", 400)

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
            return apology("deve selecionar uma ação", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("quantidade deve ser um número inteiro positivo", 400)
        except (ValueError, TypeError):
            return apology("quantidade deve ser um número inteiro", 400)

        user_shares = db.execute(
            "SELECT SUM(shares) as total FROM transactions WHERE user_id = ? AND symbol = ?",
            user_id, symbol
        )

        if not user_shares or user_shares[0]["total"] is None or user_shares[0]["total"] < shares:
            return apology("quantidade de ações insuficiente", 400)

        stock = lookup(symbol)
        if stock is None:
            return apology("símbolo inválido", 400)

        total_income = shares * stock["price"]

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_income, user_id)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            user_id, symbol, -shares, stock["price"]
        )

        flash("Venda realizada com sucesso!")
        return redirect("/")

    else:
        try:
            symbols = db.execute(
                "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
                user_id
            )
        except Exception:
            symbols = []

        return render_template("sell.html", symbols=symbols)
