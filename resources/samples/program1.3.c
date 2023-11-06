#include <stdio.h>
#include <unistd.h>

int main()
{
    pid_t ret;
    ret = fork();

    printf("ret: %d\n", ret);
    return (0);
}
