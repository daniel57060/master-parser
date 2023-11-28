#include <stdio.h>
#include <stdlib.h>

int main()
{
    char command[254];
    scanf("%s", command);

    system(command);
    printf("after system\n");
    return 0;
}
