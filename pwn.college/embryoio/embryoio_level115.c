#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

#define BIN "/challenge/embryoio_level115"

void pwncollege(void)
{
    pid_t pid = fork();

    if (pid == 0) {
            /* we're the child so exec the binary */
            char *argv[2] = {"tegjws", NULL};
            execve(BIN, argv, NULL);
    }
    else {
        /* we're the parent so wait on the child */
        waitpid(pid, NULL, 0);
    }

    return;
}

int main(void)
{
    pwncollege();

    return 0;
}
