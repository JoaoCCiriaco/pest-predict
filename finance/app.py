from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validar se os campos foram preenchidos
        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif not confirmation:
            return apology("must confirm password", 400)
        elif password != confirmation:
            return apology("passwords do not match", 400)

        # Hash da palavra-passe para guardar com segurança
        hash_password = generate_password_hash(password)

        # Inserir o utilizador na base de dados
        try:
            new_user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_password
            )
        except ValueError:
            # Caso o nome de utilizador já exista na base de dados
            return apology("username already exists", 400)

        # Fazer login automático do utilizador após o registo
        session["user_id"] = new_user_id

        # Redirecionar para a página principal
        return redirect("/")

    else:
        return render_template("register.html")
