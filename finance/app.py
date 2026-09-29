@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide stock symbol", 400)

        if not shares:
            return apology("must provide number of shares", 400)

        try:
            shares = int(shares)
        except ValueError:
            return apology("shares must be a positive integer", 400)

        if shares <= 0:
            return apology("shares must be a positive integer", 400)

        user_id = session["user_id"]

        # Check how many shares the user owns
        result = db.execute(
            "SELECT SUM(shares) AS total FROM transactions "
            "WHERE user_id = ? AND symbol = ?",
            user_id,
            symbol.upper()
        )

        owned = result[0]["total"]

        if owned is None or owned < shares:
            return apology("not enough shares", 400)

        # Get current stock price
        stock = lookup(symbol.upper())

        if stock is None:
            return apology("invalid stock symbol", 400)

        # Add money to user's cash
        total = shares * stock["price"]

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            total,
            user_id
        )

        # Record the sale as negative shares
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) "
            "VALUES (?, ?, ?, ?)",
            user_id,
            symbol.upper(),
            -shares,
            stock["price"]
        )

        return redirect("/")

    else:
        # Get stocks the user currently owns
        user_id = session["user_id"]

        symbols = db.execute(
            "SELECT symbol FROM transactions "
            "WHERE user_id = ? "
            "GROUP BY symbol "
            "HAVING SUM(shares) > 0",
            user_id
        )

        return render_template("sell.html", symbols=symbols)
