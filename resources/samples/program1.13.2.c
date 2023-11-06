#include <stdio.h>
#include <unistd.h>
#include <errno.h>

int main()
{
    printf("before exec\n");
    execl("/bin/ls", "ls", "-la", NULL);

    printf("after exec\n");
    perror("execl");
    return errno;
}
