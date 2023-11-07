#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
    printf("before fork\n"); // (1)
    fork();
    fork();
    printf("after fork\n"); //(1)
    return 0;
}
