#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>

int main()
{
    pid_t pid;
    int status, ret;

    if (fork() == 0)
    {
        printf("CHILD %d before getchar\n", getpid());
        ret = getchar();
        printf("CHILD %d after getchar\n", getpid());
        exit(ret);
    }

    printf("PARENT before wait\n");
    pid = wait(&status);
    ret = WEXITSTATUS(status);
    printf("PARENT after wait: CHILD %d ended with exit code %d\n", pid, ret);
    return 0;
}
