#include <cs50.h>
#include <stdio.h>

int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);

int main(void)
{
    // Pede ao usuário o troco em centavos (inteiro maior ou igual a 0)
    int cents;
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    // Calcula moedas de 25
    int quarters = calculate_quarters(cents);
    cents = cents - quarters * 25;

    // Calcula moedas de 10
    int dimes = calculate_dimes(cents);
    cents = cents - dimes * 10;

    // Calcula moedas de 5
    int nickels = calculate_nickels(cents);
    cents = cents - nickels * 5;

    // Calcula moedas de 1
    int pennies = calculate_pennies(cents);
    cents = cents - pennies * 1;

    // Soma e exibe o total de moedas
    int coins = quarters + dimes + nickels + pennies;
    printf("%d\n", coins);
}

int calculate_quarters(int cents)
{
    return cents / 25;
}

int calculate_dimes(int cents)
{
    return cents / 10;
}

int calculate_nickels(int cents)
{
    return cents / 5;
}

int calculate_pennies(int cents)
{
    return cents / 1;
}
