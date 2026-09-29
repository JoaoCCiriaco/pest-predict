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
            # Inserir o utilizador com o saldo inicial de 10000
            new_id = db.execute("INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)", username, hash_password, 10000.00)
        except Exception:
            return apology("nome de utilizador já existe", 400)

        session["user_id"] = new_id
        return redirect("/")

    else:
        return render_template("register.html")
