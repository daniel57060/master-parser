#include <stdio.h>
#define MAX 100

int sum(int a, int b);

int main()
{
    // Variable declarations
    int x;
    int y = 1;
    int z;

    x = (0, 1);

    // Arithmetic operators
    x = 10 + 5; // Addition
    y = x - 3;  // Subtraction
    z = x * y;  // Multiplication
    z = x / 2;  // Division
    x = x % 3;  // Modulus

    // Increment and Decrement operators
    x++; // Post-increment
    y--; // Post-decrement
    ++x; // Pre-increment
    --y; // Pre-decrement

    // Bitwise operators
    x = 5 & 3;   // Bitwise AND
    y = 5 | 3;   // Bitwise OR
    z = 5 ^ 3;   // Bitwise XOR
    x = ~5;      // Bitwise NOT
    x = 5 << 2;  // Left shift
    y = 20 >> 2; // Right shift

    // Calling functions
    int k = sum(x, y);

    // Logical operators
    if (x > 0 && y < 10)
    {
        // Logical AND
        printf("x is positive, and y is less than 10\n");
    }

    if (x < 0 || z == 15)
    {
        // Logical OR
        printf("x is negative or z is 15\n");
    }

    if (!(x == 0))
    {
        // Logical NOT
        printf("x is not equal to 0\n");
    }

    // Relational operators
    if (x == y)
    {
        printf("x is equal to y\n");
    }
    if (x != z)
    {
        printf("x is not equal to z\n");
    }
    if (x > y)
    {
        printf("x is greater than y\n");
    }
    if (x >= z)
    {
        printf("x is greater than or equal to z\n");
    }

    // Conditional (Ternary) Operator
    int result = (x > 0) ? x : y;
    printf("The result is %d\n", result);

    // Assignment operators
    x += 10;
    y -= 3;
    z *= 2;
    x /= 4;
    z %= 7;

    // Control statements
    for (int i = 0; i < 5; i++)
    {
        printf("Iteration %d\n", i);
        if (i == 1)
            continue;
        if (i == 3)
            break;
    }

    switch (x)
    {
    case 1:
        printf("x is 1\n");
        break;
    default:
        printf("x is not 1\n");
        break;
    }

    while (x > 0)
    {
        printf("x is %d\n", x);
        x--;
    }

    do
    {
        printf("This will be printed at least once\n");
    } while (z < 0);

    // Goto statement (use with caution, not recommended in most cases)
    int counter = 0;
start:
    counter++;
    if (counter < 3)
    {
        goto start;
    }

    return 0;
}

int sum(int a, int b)
{
    return a + b;
}
