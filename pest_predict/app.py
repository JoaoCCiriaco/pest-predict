from flask import Flask, render_template, request
import requests
from pest_data import PEST_DATABASE, calculate_pest_risk

app = Flask(__name__)

# Cidades principais com coordenadas pré-configuradas (São Paulo)
CITIES = {
    "Piracicaba": {"lat": -22.7253, "lon": -47.6492},
    "São Paulo": {"lat": -23.5505, "lon": -46.6333},
    "Campinas": {"lat": -22.9056, "lon": -47.0608},
    "Ribeirão Preto": {"lat": -21.1704, "lon": -47.8103},
    "Bauru": {"lat": -22.3147, "lon": -49.0606}
}

@app.route("/", methods=["GET", "POST"])
def index():
    selected_city = request.form.get("city", "Piracicaba")
    env_type = request.form.get("env_type", "Residência")

    coords = CITIES.get(selected_city, CITIES["Piracicaba"])

    # Consulta à API de Clima (Open-Meteo)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,relative_humidity_2m,rain&timezone=America/Sao_Paulo"

    weather_info = None
    results = []

    try:
        response = requests.get(url)
        data = response.json()

        weather_info = {
            "temp": data["current"]["temperature_2m"],
            "humidity": data["current"]["relative_humidity_2m"],
            "rain": data["current"]["rain"]
        }

        for pest_key, pest_info in PEST_DATABASE.items():
            score, level = calculate_pest_risk(
                pest_key=pest_key,
                temp=weather_info["temp"],
                humidity=weather_info["humidity"],
                rain_sum=weather_info["rain"],
                env_type=env_type
            )
            results.append({
                "name": pest_info["name"],
                "category": pest_info["category"],
                "score": score,
                "level": level
            })

    except Exception as e:
        print(f"Erro ao consultar clima: {e}")

    return render_template(
        "index.html",
        cities=CITIES.keys(),
        selected_city=selected_city,
        env_type=env_type,
        weather=weather_info,
        results=results
    )

if __name__ == "__main__":
    app.run(debug=True)
