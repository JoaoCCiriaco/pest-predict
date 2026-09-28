#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool only_digits(string s);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    // Verificar se o utilizador passou exatamente 1 argumento no terminal
    if (argc != 2 || !only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Converter o argumento (string) para número inteiro
    int key = atoi(argv[1]);

    // Pedir o texto simples
    string plaintext = get_string("plaintext:  ");

    printf("ciphertext: ");

    // Encriptar cada carater
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        printf("%c", rotate(plaintext[i], key));
    }
    printf("\n");

    return 0;
}

bool only_digits(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (!isdigit(s[i]))
        {
            return false;
        }
    }
    return true;
}

char rotate(char c, int n)
{
    if (isupper(c))
    {
        return (c - 'A' + n) % 26 + 'A';
    }
    else if (islower(c))
    {
        return (c - 'a' + n) % 26 + 'a';
    }
    return c;
}
