#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>

int main()
{
    pid_t ret;
    ret = fork();

    if (ret == 0)
    {
        printf("CHILD %d of the PARENT %d: ending\n", getpid(), getppid());
        exit(0);
    }

    printf("PARENT %d of the CHILD %d: press ENTER\n", getpid(), ret);
    wait(NULL);
    getchar();
    return 0;
}
