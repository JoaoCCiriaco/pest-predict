from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Municípios de São Paulo com população > 100.000 habitantes (Dados IBGE)
# Com coordenadas geográficas reais e o mosaico produtivo/predominante da região
CITIES_DATA = {
    "São Paulo": {"lat": -23.5505, "lon": -46.6333, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Guarulhos": {"lat": -23.4628, "lon": -46.5333, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Campinas": {"lat": -22.9099, "lon": -47.0626, "crop": "Citros", "crop_color": "#ff9f1c"},
    "São Bernardo do Campo": {"lat": -23.6939, "lon": -46.5650, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "São José dos Campos": {"lat": -23.1791, "lon": -45.8872, "crop": "Eucalipto", "crop_color": "#1b4332"},
    "Santo André": {"lat": -23.6639, "lon": -46.5383, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Ribeirão Preto": {"lat": -21.1704, "lon": -47.8103, "crop": "Cana-de-Açúcar", "crop_color": "#2ec4b6"},
    "Osasco": {"lat": -23.5325, "lon": -46.7917, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Sorocaba": {"lat": -23.5015, "lon": -47.4581, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Mauá": {"lat": -23.6678, "lon": -46.4614, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "São José do Rio Preto": {"lat": -20.8113, "lon": -49.3758, "crop": "Soja", "crop_color": "#7209b7"},
    "Mogi das Cruzes": {"lat": -23.5206, "lon": -46.1854, "crop": "Hortifrúti", "crop_color": "#2a9d8f"},
    "Santos": {"lat": -23.9608, "lon": -46.3339, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Diadema": {"lat": -23.6861, "lon": -46.6228, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Jundiaí": {"lat": -23.1857, "lon": -46.8892, "crop": "Fruticultura", "crop_color": "#e76c00"},
    "Piracicaba": {"lat": -22.7258, "lon": -47.6476, "crop": "Cana-de-Açúcar", "crop_color": "#2ec4b6"},
    "Carapicuíba": {"lat": -23.5222, "lon": -46.8361, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Bauru": {"lat": -22.3149, "lon": -49.0606, "crop": "Milho", "crop_color": "#ffb703"},
    "Itaquaquecetuba": {"lat": -23.4861, "lon": -46.3483, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "São Vicente": {"lat": -23.9631, "lon": -46.3919, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Franca": {"lat": -20.5386, "lon": -47.4008, "crop": "Café", "crop_color": "#6f4e37"},
    "Praia Grande": {"lat": -24.0058, "lon": -46.4028, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Guarujá": {"lat": -23.9931, "lon": -46.2564, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Taubaté": {"lat": -23.0264, "lon": -45.5553, "crop": "Arroz/Pastagem", "crop_color": "#e9c46a"},
    "Limeira": {"lat": -22.5647, "lon": -47.4017, "crop": "Citros", "crop_color": "#ff9f1c"},
    "Suzano": {"lat": -23.5425, "lon": -46.3108, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Paulínia": {"lat": -22.7611, "lon": -47.1539, "crop": "Cana-de-Açúcar", "crop_color": "#2ec4b6"},
    "Sumaré": {"lat": -22.8206, "lon": -47.2669, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Barueri": {"lat": -23.5111, "lon": -46.8761, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Embu das Artes": {"lat": -23.6489, "lon": -46.8522, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Indaiatuba": {"lat": -23.0903, "lon": -47.2181, "crop": "Hortifrúti", "crop_color": "#2a9d8f"},
    "Cotia": {"lat": -23.6039, "lon": -46.9192, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Americana": {"lat": -22.7392, "lon": -47.3314, "crop": "Cana-de-Açúcar", "crop_color": "#2ec4b6"},
    "Marília": {"lat": -22.2139, "lon": -49.9458, "crop": "Café/Pastagem", "crop_color": "#6f4e37"},
    "Araraquara": {"lat": -21.7944, "lon": -48.1758, "crop": "Citros/Cana", "crop_color": "#ff9f1c"},
    "Jacareí": {"lat": -23.3053, "lon": -45.9658, "crop": "Eucalipto", "crop_color": "#1b4332"},
    "Presidente Prudente": {"lat": -22.1256, "lon": -51.3889, "crop": "Soja", "crop_color": "#7209b7"},
    "Itapevi": {"lat": -23.5489, "lon": -46.9342, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Hortolândia": {"lat": -22.8583, "lon": -47.2200, "crop": "Área Urbana", "crop_color": "#6c757d"},
    "Rio Claro": {"lat": -22.4114, "lon": -47.5614, "crop": "Cana-de-Açúcar", "crop_color": "#2ec4b6"},
    "Botucatu": {"lat": -22.8858, "lon": -48.4450, "crop": "Eucalipto", "crop_color": "#1b4332"},
    "Araçatuba": {"lat": -21.2089, "lon": -50.4328, "crop": "Cana/Pecuária", "crop_color": "#2ec4b6"},
    "São Carlos": {"lat": -21.9981, "lon": -47.8908, "crop": "Eucalipto/Cana", "crop_color": "#1b4332"}
}

# Catálogo Completo de Pragas Urbanas, Agrícolas e Florestais
PESTS = {
    "urban": [
        {"key": "escorpiao_amarelo", "name": "Escorpião-amarelo (Tityus serrulatus)"},
        {"key": "aedes_aegypti", "name": "Aedes aegypti (Dengue/Zika/Chikungunya)"},
        {"key": "barata_esgoto", "name": "Barata-de-esgoto (Periplaneta americana)"},
        {"key": "blattella_germanica", "name": "Barata-germânica / Alemã (Blattella germanica)"},
        {"key": "cupim_subterraneo", "name": "Cupim Subterrâneo (Coptotermes gestroi)"}
    ],
    "agri": [
        {"key": "sauva_parda", "name": "Saúva-parda / Formiga-cortadeira (Atta capiguara)"},
        {"key": "quenquem_minadora", "name": "Quenquém-minadora (Acromyrmex lundi)"},
        {"key": "broca_cana", "name": "Broca-da-cana (Diatraea saccharalis)"},
        {"key": "lagarta_parda", "name": "Lagarta-parda do Eucalipto (Thyrinteina arnobia)"},
        {"key": "percevejo_castanho", "name": "Percevejo-castanho da Soja/Milho"},
        {"key": "psilideo_citros", "name": "Psilídeo dos Citros (Diaphorina citri)"},
        {"key": "cigarrinha_milho", "name": "Cigarrinha-do-milho (Dalbulus maidis)"},
        {"key": "bicudo_algodoeiro", "name": "Bicudo-do-algodoeiro (Anthonomus grandis)"},
        {"key": "mosca_frutas", "name": "Mosca-das-frutas (Ceratitis capitata)"}
    ]
}

def get_risk_level(score):
    if score >= 75:
        return "Risco Crítico / Alto"
    elif score >= 50:
        return "Risco Moderado"
    elif score >= 30:
        return "Risco Baixo-Médio"
    else:
        return "Risco Baixo"

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_city = "Piracicaba"
    env_type = "Cana-de-Açúcar"

    if request.method == 'POST':
        selected_city = request.form.get('city', selected_city)
        env_type = request.form.get('env_type', env_type)

    # Dados meteorológicos simulados da região (Open-Meteo)
    weather = {
        "temp": round(random.uniform(24.0, 31.5), 1),
        "humidity": random.randint(58, 88),
        "rain": round(random.uniform(0.0, 25.0), 1)
    }

    # Gerar scores para pragas urbanas
    urban_results = []
    for pest in PESTS["urban"]:
        score = random.randint(35, 95)
        urban_results.append({
            "key": pest["key"],
            "name": pest["name"],
            "score": score,
            "level": get_risk_level(score)
        })

    # Gerar scores para pragas agrícolas
    agri_results = []
    for pest in PESTS["agri"]:
        score = random.randint(40, 98)
        agri_results.append({
            "key": pest["key"],
            "name": pest["name"],
            "score": score,
            "level": get_risk_level(score)
        })

    return render_template(
        'index.html',
        cities=list(CITIES_DATA.keys()),
        selected_city=selected_city,
        env_type=env_type,
        weather=weather,
        urban_results=urban_results,
        agri_results=agri_results
    )

# API para devolver os pontos e manchas de calor no Leaflet
@app.route('/api/pest_map/<pest_key>')
def get_pest_map(pest_key):
    map_points = []
    random.seed(hash(pest_key) % 10000)  # Mantém a consistência visual dos pontos por praga

    for city_name, data in CITIES_DATA.items():
        score = random.randint(30, 95)
        map_points.append({
            "city": city_name,
            "lat": data["lat"],
            "lon": data["lon"],
            "crop": data["crop"],
            "crop_color": data["crop_color"],
            "score": score
        })

    return jsonify(map_points)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
