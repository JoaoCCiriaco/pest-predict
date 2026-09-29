#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;
const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // Verificar se o utilizador passou exatamente 1 argumento
    if (argc != 2)
    {
        printf("Usage: ./recover card.raw\n");
        return 1;
    }

    // Abrir o cartão de memória
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Buffer para armazenar blocos de 512 bytes
    BYTE buffer[BLOCK_SIZE];

    // Ficheiro de saída para as imagens JPEG recuperadas
    FILE *outimg = NULL;

    // Nome do ficheiro gerado (ex: "000.jpg")
    char filename[8];

    // Contador de JPEGs encontrados
    int img_count = 0;

    // Ler blocos de 512 bytes continuamente até ao fim do ficheiro
    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        // Verificar se o bloco marca o início de um novo JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Se já tínhamos um JPEG aberto, fecha-se
            if (outimg != NULL)
            {
                fclose(outimg);
            }

            // Criar o nome do ficheiro numerado (000.jpg, 001.jpg, etc.)
            sprintf(filename, "%03i.jpg", img_count);

            // Abrir o novo ficheiro para escrita
            outimg = fopen(filename, "w");

            // Incrementar o contador
            img_count++;
        }

        // Se um ficheiro JPEG estiver atualmente aberto, escreve-se nele o bloco
        if (outimg != NULL)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, outimg);
        }
    }

    // Fechar o último ficheiro de imagem se tiver ficado aberto
    if (outimg != NULL)
    {
        fclose(outimg);
    }

    // Fechar o cartão de memória
    fclose(card);

    return 0;
}
