import os
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
            "SELECT SUM(shares) AS total FROM transactions "
            "WHERE user_id = ? AND symbol = ?",
            user_id, symbol
        )

        owned = result[0]["total"]

        if owned is None or owned < shares:
            return apology("not enough shares", 400)

        total = shares * stock["price"]

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            total, user_id
        )

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) "
            "VALUES (?, ?, ?, ?)",
            user_id, symbol, -shares, stock["price"]
        )

        return redirect("/")

    symbols = db.execute(
        "SELECT symbol FROM transactions "
        "WHERE user_id = ? "
        "GROUP BY symbol "
        "HAVING SUM(shares) > 0",
        user_id
    )

    return render_template("sell.html", symbols=symbols)
