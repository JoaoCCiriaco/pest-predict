import csv
import sys


def main():

    # 1. Verificar os argumentos da linha de comandos
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # 2. Ler o ficheiro da base de dados CSV para uma lista de dicionários
    database = []
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        # Obter os nomes de todas as STRs (todas as colunas exceto 'name')
        strs = reader.fieldnames[1:]
        for row in reader:
            database.append(row)

    # 3. Ler a sequência de ADN do ficheiro TXT
    with open(sys.argv[2], "r") as file:
        dna_sequence = file.read()

    # 4. Encontrar a maior repetição de cada STR na sequência de ADN
    str_counts = {}
    for str_name in strs:
        str_counts[str_name] = longest_match(dna_sequence, str_name)

    # 5. Procurar uma correspondência na base de dados
    for person in database:
        match = True
        for str_name in strs:
            if int(person[str_name]) != str_counts[str_name]:
                match = False
                break

        if match:
            print(person["name"])
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):

        count = 0

        while True:

            start = i + count * subsequence_length
            end = start + subsequence_length

            if sequence[start:end] == subsequence:
                count += 1
            else:
                break

        longest_run = max(longest_run, count)

    return longest_run


if __name__ == "__main__":
    main()
