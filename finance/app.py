import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]

    rows = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares "
        "FROM transactions WHERE user_id = ? "
        "GROUP BY symbol HAVING total_shares > 0",
        user_id
    )

    cash = db.execute(
        "SELECT cash FROM users WHERE id = ?",
        user_id
    )[0]["cash"]

    stocks = []
    total = cash

    for row in rows:
        stock = lookup(row["symbol"])

        if stock:
            value = stock["price"] * row["total_shares"]
            total += value

            stocks.append({
                "symbol": row["symbol"],
                "shares": row["total_shares"],
                "price": stock["price"],
                "total": value
            })

    return render_template(
        "index.html",
        stocks=stocks,
        cash=cash,
        total=total
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide stock symbol", 400)

        stock = lookup(symbol.upper())

        if stock is None:
            return apology("invalid stock symbol", 400)

        try:
            shares = int(shares)
        except (ValueError, TypeError):
            return apology("shares must be a positive integer", 400)

        if shares <= 0:
            return apology("shares must be a positive integer", 400)

        user_id = session["user_id"]

        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?",
            user_id
        )[0]["cash"]

        total = shares * stock["price"]

        if cash < total:
            return apology("not enough money", 400)

        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?",
            total,
            user_id
        )

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) "
            "VALUES (?, ?, ?, ?)",
            user_id,
            stock["symbol"],
            shares,
            stock["price"]
        )

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]

    transactions = db.execute(
        "SELECT symbol, shares, price, transacted "
        "FROM transactions WHERE user_id = ? "
        "ORDER BY transacted DESC",
        user_id
    )

    return render_template(
        "history.html",
        transactions=transactions
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username", 400)

        if not password:
            return apology("must provide password", 400)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            username
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password
        ):
            return apology("invalid username and/or password", 400)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide stock symbol", 400)

        stock = lookup(symbol.upper())

        if stock is None:
            return apology("invalid stock symbol", 400)

        return render_template("quoted.html", stock=stock)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)

        if not password:
            return apology("must provide password", 400)

        if not confirmation:
            return apology("must confirm password", 400)

        if password != confirmation:
            return apology("passwords do not match", 400)

        password_hash = generate_password_hash(password)

        try:
            user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                password_hash
            )
        except Exception:
            return apology("username already exists", 400)

        session["user_id"] = user_id

        return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide stock symbol", 400)

        try:
            shares = int(shares)
        except (ValueError, TypeError):
            return apology("shares must be a positive integer", 400)

        if shares <= 0:
            return apology("shares must be a positive integer", 400)

        symbol = symbol.upper()

        stock = lookup(symbol)

        if stock is None:
            return apology("invalid stock symbol", 400)

        result = db.execute(
            "SELECT SUM(shares) AS total "
            "FROM transactions "
            "WHERE user_id = ? AND symbol = ?",
            user_id,
            symbol
        )

        owned = result[0]["total"]

        if owned is None or owned < shares:
            return apology("not enough shares", 400)

        total = shares * stock["price"]

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            total,
            user_id
        )

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) "
            "VALUES (?, ?, ?, ?)",
            user_id,
            symbol,
            -shares,
            stock["price"]
        )

        return redirect("/")

    symbols = db.execute(
        "SELECT symbol FROM transactions "
        "WHERE user_id = ? "
        "GROUP BY symbol "
        "HAVING SUM(shares) > 0",
        user_id
    )

    return render_template(
        "sell.html",
        symbols=symbols
    )
