#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

#define BIN_NAME "/challenge/embryoio_level85"

void pwncollege(void) { return; }

int main(void)
{
    pid_t pid = fork();

    switch (pid)
    {
        case -1:
        {
            perror("fork()");
            return EXIT_FAILURE;
            break;
        }
        case 0:
        {
            /* we're the child */
            char *argv[2] = {BIN_NAME, NULL};

            chdir("/tmp/pmjmky");
            execve(argv[0], argv, NULL);

            return EXIT_FAILURE;
            break;
        }
        default:
        {
            /* we're the parent so wait on the child */
            waitpid(pid, NULL, 0);
            break;
        }
    }

    return EXIT_SUCCESS;
}
