// Modifica o volume de um ficheiro de áudio WAV

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Número de bytes no cabeçalho de um ficheiro WAV
const int HEADER_SIZE = 44;

typedef uint8_t BYTE;
typedef int16_t SAMPLE;

int main(int argc, char *argv[])
{
    // Verificar argumentos de linha de comando
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Abrir ficheiro de entrada
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Abrir ficheiro de saída
    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        fclose(input);
        return 1;
    }

    float factor = atof(argv[3]);

    // Copiar o cabeçalho do ficheiro de entrada para o ficheiro de saída
    BYTE header[HEADER_SIZE];
    fread(header, sizeof(BYTE), HEADER_SIZE, input);
    fwrite(header, sizeof(BYTE), HEADER_SIZE, output);

    // Ler amostras do ficheiro de entrada, ajustar o volume e escrever no ficheiro de saída
    SAMPLE buffer;
    while (fread(&buffer, sizeof(SAMPLE), 1, input) == 1)
    {
        buffer = buffer * factor;
        fwrite(&buffer, sizeof(SAMPLE), 1, output);
    }

    // Fechar ficheiros abertos
    fclose(input);
    fclose(output);
}
