#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Pontuação atribuída a cada letra do alfabeto (A-Z)
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Pedir a palavra a cada um dos dois jogadores
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Calcular as pontuações
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Imprimir o vencedor
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    int score = 0;

    // Percorrer cada carater da palavra
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        if (isupper(word[i]))
        {
            score += POINTS[word[i] - 'A'];
        }
        else if (islower(word[i]))
        {
            score += POINTS[word[i] - 'a'];
        }
    }

    return score;
}
