#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Número máximo de candidatos
#define MAX 9

// Candidatos têm nome e contagem de votos
typedef struct
{
    string name;
    int votes;
} candidate;

// Array de candidatos
candidate candidates[MAX];

// Número de candidatos
int candidate_count;

// Protótipos de funções
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Verificar uso correto
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Preencher array de candidatos
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[1 + i];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop para todos os eleitores
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Verificar se o voto é válido
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Imprimir o vencedor da eleição
    print_winner();
}

// Atualizar totais de votos para um novo voto
bool vote(string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

// Imprimir o vencedor (ou vencedores) da eleição
void print_winner(void)
{
    int max_votes = 0;

    // Encontrar o maior número de votos
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > max_votes)
        {
            max_votes = candidates[i].votes;
        }
    }

    // Imprimir todos os candidatos que têm o maior número de votos
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes == max_votes)
        {
            printf("%s\n", candidates[i].name);
        }
    }
}

