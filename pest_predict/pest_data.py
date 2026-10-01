import datetime

# Base de Dados de Pragas com Parâmetros Biológicos
PEST_DATABASE = {
    "escorpiao_amarelo": {
        "name": "Escorpião-Amarelo (Tityus serrulatus)",
        "category": "Urbana",
        "breeding_months": [10, 11, 12, 1, 2, 3],  # Outubro a Março
        "ideal_temp_min": 24.0,
        "ideal_temp_max": 34.0,
        "min_humidity": 65,
        "rain_threshold_mm": 20.0,
        "high_risk_environments": ["Residência", "Comércio", "Próximo a APP/Córrego"]
    },
    "aedes_aegypti": {
        "name": "Mosquito da Dengue (Aedes aegypti)",
        "category": "Urbana",
        "breeding_months": [11, 12, 1, 2, 3, 4],  # Novembro a Abril
        "ideal_temp_min": 25.0,
        "ideal_temp_max": 31.0,
        "min_humidity": 70,
        "rain_threshold_mm": 10.0,
        "high_risk_environments": ["Residência", "Comércio", "Próximo a Córrego"]
    },
    "lagarta_eucalipto": {
        "name": "Lagarta-Parda do Eucalipto (Thyrinteina arnobia)",
        "category": "Agrícola/Florestal",
        "breeding_months": [9, 10, 11, 12],  # Setembro a Dezembro
        "ideal_temp_min": 22.0,
        "ideal_temp_max": 28.0,
        "min_humidity": 60,
        "rain_threshold_mm": 10.0,
        "high_risk_environments": ["Eucalipto"]
    }
}

def calculate_pest_risk(pest_key, temp, humidity, rain_sum, env_type):
    """
    Calcula o nível de risco (0 a 100%) para uma praga com base no clima e ambiente.
    """
    if pest_key not in PEST_DATABASE:
        return 0, "Praga não encontrada"

    pest = PEST_DATABASE[pest_key]
    score = 0
    current_month = datetime.datetime.now().month

    # 1. Avaliação de Sazonalidade Reprodutiva (Peso: 30%)
    if current_month in pest["breeding_months"]:
        score += 30

    # 2. Avaliação de Temperatura (Peso: 25%)
    if pest["ideal_temp_min"] <= temp <= pest["ideal_temp_max"]:
        score += 25
    elif abs(temp - pest["ideal_temp_min"]) <= 3:
        score += 10

    # 3. Avaliação de Humidade (Peso: 20%)
    if humidity >= pest["min_humidity"]:
        score += 20

    # 4. Avaliação de Precipitação/Chuva (Peso: 15%)
    if rain_sum >= pest["rain_threshold_mm"]:
        score += 15

    # 5. Avaliação do Tipo de Ambiente/Cliente (Peso: 10%)
    if env_type in pest["high_risk_environments"]:
        score += 10

    # Definição do Nível de Alerta
    if score >= 75:
        level = "CRÍTICO (Alerta Vermelho)"
    elif score >= 50:
        level = "ALTO (Alerta Laranja)"
    elif score >= 30:
        level = "MÉDIO (Alerta Amarelo)"
    else:
        level = "BAIXO (Alerta Verde)"

    return score, level
