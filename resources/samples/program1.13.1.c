#include <stdio.h>
#include <unistd.h>
#include <errno.h>

int main()
{
    printf("before exec\n");
    execl("/bin/ls", "ls", NULL);

    printf("after exec\n");
    perror("execl");
    return errno;
}
