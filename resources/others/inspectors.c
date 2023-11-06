void main()
{
    if (1)
    {
        fork();
        wait();
        waitpid(pid, &status);
        printf("Hello World\n");
        exit(0);
    }
}
