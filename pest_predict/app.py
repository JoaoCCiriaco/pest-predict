import json
from flask import Flask, render_template, request, jsonify
import requests
from pest_data import PEST_DATABASE, calculate_pest_risk

app = Flask(__name__)

# Carrega a lista de municípios do JSON
with open("cities_sp.json", "r", encoding="utf-8") as f:
    CITIES = json.load(f)

# Definição das Macro-Regiões Predominantes de Culturas em SP para o Mosaico
CROP_REGIONS = {
    "Ribeirão Preto": {"crop": "Cana-de-Açúcar", "color": "#2ec4b6"},
    "Piracicaba": {"crop": "Cana-de-Açúcar", "color": "#2ec4b6"},
    "Araraquara": {"crop": "Cana-de-Açúcar", "color": "#2ec4b6"},
    "Limeira": {"crop": "Citros", "color": "#ff9f1c"},
    "Barretos": {"crop": "Citros", "color": "#ff9f1c"},
    "Botucatu": {"crop": "Eucalipto", "color": "#1b4332"},
    "Itapetininga": {"crop": "Eucalipto", "color": "#1b4332"},
    "São José dos Campos": {"crop": "Eucalipto", "color": "#1b4332"},
    "Marília": {"crop": "Soja", "color": "#7209b7"},
    "Presidente Prudente": {"crop": "Soja", "color": "#7209b7"},
    "Itapeva": {"crop": "Soja", "color": "#7209b7"},
    "Bauru": {"crop": "Milho", "color": "#ffb703"},
    "Araçatuba": {"crop": "Milho", "color": "#ffb703"},
    "São Paulo": {"crop": "Urbana", "color": "#6c757d"},
    "Campinas": {"crop": "Urbana", "color": "#6c757d"},
    "Santos": {"crop": "Urbana", "color": "#6c757d"}
}

@app.route("/", methods=["GET", "POST"])
def index():
    selected_city = request.form.get("city", "Piracicaba")
    env_type = request.form.get("env_type", "Residência")

    coords = CITIES.get(selected_city, CITIES["Piracicaba"])

    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,relative_humidity_2m&daily=rain_sum&timezone=America/Sao_Paulo"

    weather_info = None
    urban_results = []
    agri_results = []

    try:
        response = requests.get(url)
        data = response.json()

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
                "key": pest_key,
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
        cities=sorted(CITIES.keys()),
        selected_city=selected_city,
        env_type=env_type,
        weather=weather_info,
        urban_results=urban_results,
        agri_results=agri_results
    )

# Rota de dados geográficos e calor para os mapas
@app.route("/api/pest_map/<pest_key>")
def pest_map_data(pest_key):
    map_data = []
    for city_name, coords in CITIES.items():
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,relative_humidity_2m&daily=rain_sum&timezone=America/Sao_Paulo"
            res = requests.get(url).json()
            temp = res["current"]["temperature_2m"]
            humidity = res["current"]["relative_humidity_2m"]
            rain = res["daily"]["rain_sum"][0] if "daily" in res and "rain_sum" in res["daily"] else 0.0

            score, level = calculate_pest_risk(pest_key, temp, humidity, rain, "Residência")

            crop_info = CROP_REGIONS.get(city_name, {"crop": "Outras", "color": "#adb5bd"})

            map_data.append({
                "city": city_name,
                "lat": coords["lat"],
                "lon": coords["lon"],
                "score": score,
                "level": level,
                "crop": crop_info["crop"],
                "crop_color": crop_info["color"]
            })
        except Exception:
            continue

    return jsonify(map_data)

if __name__ == "__main__":
    app.run(debug=True)
