#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>

int main()
{
    pid_t pid_second_child;

    if (fork() == 0)
    {
        printf("first CHILD before exit\n");
        exit(0);
    }

    pid_second_child = fork();
    if (pid_second_child == 0)
    {
        printf("second CHILD before getchar\n");
        getchar(); // what would happen without getchar ?
        printf("second CHILD after getchar\n");
        exit(0);
    }

    printf("PARENT before waitpid\n");
    waitpid(pid_second_child, NULL, 0); // PARENT blocks until second CHILD ends
    printf("PARENT after waitpid\n");
    return 0;
}
