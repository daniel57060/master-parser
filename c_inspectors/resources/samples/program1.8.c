#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

int main()
{
    int i, n;

    printf("Number of levels of the process tree ?");
    scanf("%d", &n);

    for (i = 1; i <= n; i++)
    {
        fork();
        printf("i=%d \t pid=%d\n", i, getpid());
    }

    return 0;
}
