@app.route("/", methods=["GET", "POST"])
def index():
    selected_city = request.form.get("city", "Piracicaba")
    env_type = request.form.get("env_type", "Residência")

    coords = CITIES.get(selected_city, CITIES["Piracicaba"])

    # Adicionamos 'daily=rain_sum' para pegar a soma de chuva acumulada do dia
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,relative_humidity_2m&daily=rain_sum&timezone=America/Sao_Paulo"

    weather_info = None
    urban_results = []
    agri_results = []

    try:
        response = requests.get(url)
        data = response.json()

        # Pega a chuva acumulada do dia de hoje (índice 0 do daily)
        rain_today = data["daily"]["rain_sum"][0] if "daily" in data and "rain_sum" in data["daily"] else 0.0

        weather_info = {
            "temp": data["current"]["temperature_2m"],
            "humidity": data["current"]["relative_humidity_2m"],
            "rain": rain_today
        }

        for pest_key, pest_info in PEST_DATABASE.items():
            score, level = calculate_pest_risk(
                pest_key=pest_key,
                temp=weather_info["temp"],
                humidity=weather_info["humidity"],
                rain_sum=weather_info["rain"],
                env_type=env_type
            )

            item = {
                "name": pest_info["name"],
                "category": pest_info["category"],
                "score": score,
                "level": level
            }

            if pest_info["category"] == "Urbana":
                urban_results.append(item)
            else:
                agri_results.append(item)

    except Exception as e:
        print(f"Erro ao consultar clima: {e}")

    return render_template(
        "index.html",
        cities=CITIES.keys(),
        selected_city=selected_city,
        env_type=env_type,
        weather=weather_info,
        urban_results=urban_results,
        agri_results=agri_results
    )
