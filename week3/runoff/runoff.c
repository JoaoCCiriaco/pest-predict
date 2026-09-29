#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Numéro máximo de eleitores e candidatos
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] é a j-ésima preferência do eleitor i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidato tem nome, contagem de votos e estado de eliminação
typedef struct
{
    string name;
    int votes;
    bool eliminated;
} candidate;

// Array de candidatos
candidate candidates[MAX_CANDIDATES];

// Número de eleitores e candidatos
int voter_count;
int candidate_count;

// Protótipos das funções
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Verificar utilização inválida
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Registar número de candidatos
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[1 + i];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Registar votos
    for (int i = 0; i < voter_count; i++)
    {

        // Registar preferência para cada candidato
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            // Verificar se o voto é válido
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Continuar o processo até haver um vencedor ou empate
    while (true)
    {
        // Calcular votos dos candidatos não eliminados
        tabulate();

        // Verificar se alguém venceu
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Encontrar menor número de votos
        int min = find_min();
        bool tie = is_tie(min);

        // Se houver empate entre todos, todos os restantes vencem
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminar candidatos com o menor número de votos
        eliminate(min);

        // Resetar contagem de votos para a próxima volta
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }
    return 0;
}

// 1. Registar a preferência se o candidato for válido
bool vote(int voter, int rank, string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            preferences[voter][rank] = i;
            return true;
        }
    }
    return false;
}

// 2. Tabular votos para candidatos ativos
void tabulate(void)
{
    for (int i = 0; i < voter_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            int idx = preferences[i][j];
            if (!candidates[idx].eliminated)
            {
                candidates[idx].votes++;
                break;
            }
        }
    }
}

// 3. Imprimir vencedor se tiver mais de 50% dos votos
bool print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > voter_count / 2)
        {
            printf("%s\n", candidates[i].name);
            return true;
        }
    }
    return false;
}

// 4. Retornar o menor número de votos entre os candidatos ativos
int find_min(void)
{
    int min = voter_count;
    for (int i = 0; i < candidate_count; i++)
    {
        if (!candidates[i].eliminated && candidates[i].votes < min)
        {
            min = candidates[i].votes;
        }
    }
    return min;
}

// 5. Verificar se todos os candidatos ativos estão empatados
bool is_tie(int min)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (!candidates[i].eliminated && candidates[i].votes != min)
        {
            return false;
        }
    }
    return true;
}

// 6. Eliminar o(s) candidato(s) com menor número de votos
void eliminate(int min)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes == min)
        {
            candidates[i].eliminated = true;
        }
    }
}
