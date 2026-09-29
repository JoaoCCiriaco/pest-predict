// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table
const unsigned int N = 65536;

// Hash table
node *table[N];

// Total word count loaded
unsigned int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash word to get index
    unsigned int index = hash(word);

    // Search linked list at table[index]
    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // DJB2 Hash Algorithm
    unsigned long hash_val = 5381;
    int c;
    while ((c = tolower(*word++)))
    {
        hash_val = ((hash_val << 5) + hash_val) + c;
    }
    return hash_val % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        return false;
    }

    // Buffer to store current word
    char buffer[LENGTH + 1];

    // Read words from file
    while (fscanf(source, "%45s", buffer) != EOF)
    {
        // Allocate memory for new node
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            fclose(source);
            return false;
        }

        // Copy word into node
        strcpy(n->word, buffer);

        // Hash word to find bucket
        unsigned int index = hash(buffer);

        // Insert node into hash table at head of linked list
        n->next = table[index];
        table[index] = n;

        // Keep track of total words
        word_count++;
    }

    // Close file
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Traverse each bucket in hash table
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
