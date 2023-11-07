#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

int main()
{
    int i, n;

    printf("Number of children? ");
    scanf("%d", &n);

    for (i = 1; i <= n; i++)
    {
        if (fork() == 0)
        {
            printf("CHILD %d ends\n", getpid());
            exit(0);
        }
        printf("PARENT %d continues\n", getpid());
    }

    return 0;
}
