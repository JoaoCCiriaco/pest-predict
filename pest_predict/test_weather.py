import requests
from pest_data import PEST_DATABASE, calculate_pest_risk

# Coordenadas geográficas de Piracicaba / SP (Exemplo)
LATITUDE = -22.7253
LONGITUDE = -47.6492

# Consulta à API Open-Meteo
url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=temperature_2m,relative_humidity_2m,rain&daily=rain_sum&timezone=America/Sao_Paulo"

try:
    response = requests.get(url)
    data = response.json()

    # Extrair dados climáticos atuais
    temp = data["current"]["temperature_2m"]
    humidity = data["current"]["relative_humidity_2m"]
    rain_today = data["current"]["rain"]

    print("=" * 50)
    print("DADOS METEOROLÓGICOS ATUAIS (PIRACICABA/SP)")
    print(f"Temperatura: {temp}°C")
    print(f"Humidade do Ar: {humidity}%")
    print(f"Chuva Atual: {rain_today} mm")
    print("=" * 50)
    print("\nANÁLISE PREDITIVA DE PRAGAS:")

    # Testar previsão para todas as pragas da base de dados
    for pest_key, pest_info in PEST_DATABASE.items():
        score, level = calculate_pest_risk(
            pest_key=pest_key,
            temp=temp,
            humidity=humidity,
            rain_sum=rain_today,
            env_type="Residência"
        )
        print(f"\nPraga: {pest_info['name']}")
        print(f"  > Risco Calculado: {score}%")
        print(f"  > Status: {level}")

except Exception as e:
    print(f"Erro ao consultar a API meteorológica: {e}")
