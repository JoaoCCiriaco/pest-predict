from cs50 import get_float

# Solicitar troco válido (não negativo)
while True:
    dollars = get_float("Change owed: ")
    if dollars >= 0:
        break

# Converter dólares para cêntimos para evitar problemas de precisão de ponto flutuante
cents = round(dollars * 100)

coins = 0

# Moedas disponíveis: 25, 10, 5, 1 cêntimos
for coin in [25, 10, 5, 1]:
    coins += cents // coin
    cents %= coin

print(coins)
