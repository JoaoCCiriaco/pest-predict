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
        try:
            symbols = db.execute(
                "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
                user_id
            )
        except Exception:
            symbols = []

        return render_template("sell.html", symbols=symbols)
