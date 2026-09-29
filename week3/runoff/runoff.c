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
        return A mensagem `can't check until a frown turns upside down` surge no `check50` quando o primeiro teste falha, o que faz com que todos os testes seguintes sejam cancelados. Isso significa que o ficheiro `runoff.c` não tem o código fonte em C completo no topo (a função `main` e a declaração de variáveis globais).

Para resolver isto de forma definitiva, vamos substituir o conteúdo do ficheiro pelo código base e submeter:

---

### Passo 1: Limpar o ficheiro

1. Abre o ficheiro `runoff.c` no editor na parte superior.
2. Seleciona todo o conteúdo com **Ctrl + A** (ou **Cmd + A**) e apaga para deixar a página em branco.

---

### Passo 2: Adicionar a estrutura e a lógica do Runoff

Copia o código completo abaixo para o `runoff.c`. Ele inclui as bibliotecas, a função `main` do CS50 e a implementação das 6 funções:

- **`vote`**: Procura o candidato pelo nome e guarda o seu índice na matriz `preferences` do eleitor.
- **`tabulate`**: Incrementa a contagem de votos do candidato ativo com maior preferência de cada eleitor.
- **`print_winner`**: Imprime o nome do candidato se este tiver mais de metade do total dos votos (`voter_count / 2`).
- **`find_min`**: Procura a menor quantidade de votos entre todos os candidatos não eliminados.
- **`is_tie`**: Confirma se todos os candidatos ativos partilham exatamente a mesma quantidade de votos `min`.
- **`eliminate`**: Modifica a propriedade `eliminated` para `true` nos candidatos cuja contagem de votos seja igual a `min`.

```c
#include <cs50.h>
#include <stdio.h>
#include <string.h>

#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

int preferences[MAX_VOTERS][MAX_CANDIDATES];

typedef struct
{
