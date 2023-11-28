#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
    int i, j;
    i = 1;
    j = 1;

    do
    {
        if (fork() > 0)
        {
            j += 1;
        }
        else
        {
            j += 2;
        }
        i++;
    } while (i < 2 || j < 3);

    return 0;
}
