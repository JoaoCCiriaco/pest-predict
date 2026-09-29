from cs50 import get_string


def main():
    # Pedir o texto ao utilizador
    text = get_string("Text: ")

    # Contar letras, palavras e frases
    letters = 0
    words = 0
    sentences = 0

    if len(text) > 0:
        words = 1

    for char in text:
        if char.isalpha():
            letters += 1
        elif char == " ":
            words += 1
        elif char in [".", "!", "?"]:
            sentences += 1

    # Cálculos das médias por 100 palavras
    L = (letters / words) * 100
    S = (sentences / words) * 100

    # Índice Coleman-Liau
    index = round(0.0588 * L - 0.296 * S - 15.8)

    # Nível do texto
    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


if __name__ == "__main__":
    main()
