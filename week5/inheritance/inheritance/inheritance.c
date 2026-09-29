person *create_family(int generations)
{
    // 1. Alocar memória para uma nova pessoa
    person *p = malloc(sizeof(person));
    if (p == NULL)
    {
        return NULL;
    }

    // 2. Se ainda houver gerações de pais a criar
    if (generations > 1)
    {
        // Criar pais recursivamente
        p->parents[0] = create_family(generations - 1);
        p->parents[1] = create_family(generations - 1);

        // Escolher aleatoriamente um alelo de cada pai
        p->alleles[0] = p->parents[0]->alleles[rand() % 2];
        p->alleles[1] = p->parents[1]->alleles[rand() % 2];
    }
    // 3. Se for a geração mais antiga (geração base)
    else
    {
        p->parents[0] = NULL;
        p->parents[1] = NULL;
        p->alleles[0] = random_allele();
        p->alleles[1] = random_allele();
    }

    // 4. Retornar a pessoa criada
    return p;
}
void free_family(person *p)
{
    // Caso base: se o ponteiro for nulo, não há nada a libertar
    if (p == NULL)
    {
        return;
    }

    // Libertar os pais recursivamente
    free_family(p->parents[0]);
    free_family(p->parents[1]);

    // Libertar a pessoa atual
    free(p);
}
