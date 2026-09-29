#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    string name;
    int votes;
    bool eliminated;
} candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

Para resolver o **`runoff.c`** de forma completa e sem gerar problemas de compilação, vamos entender como a estrutura funciona e como podes preencher o código.

O CS50 fornece a estrutura base do programa (com as diretivas `#include`, a definição das estruturas de dados e a função `main`). O teu trabalho é implementar a lógica das 6 funções essenciais que ficam na parte inferior do ficheiro.

---

### Passo 1: Garantir o ficheiro limpo

No terminal (na parte inferior do VS Code), corre estes comandos para descarregar o ficheiro base oficial do CS50:

```bash
cd /workspaces/310188652/week3/runoff
wget [https://cdn.cs50.net/2023/fall/psets/3/runoff.zip](https://cdn.cs50.net/2023/fall/psets/3/runoff.zip) && unzip -o runoff.zip && rm runoff.zip
code runoff.c
