#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    // Pede ao utilizador uma altura entre 1 e 8
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Constrói a pirâmide linha a linha
    for (int i = 0; i < height; i++)
    {
        // Imprime os espaços em branco para alinhar à direita
        for (int j = 0; j < height - i - 1; j++)
        {
            printf(" ");
        }

        // Imprime os cardinal (#)
        for (int k = 0; k <= i; k++)
        {
            printf("#");
        }

        // Nova linha
        printf("\n");
    }
}
