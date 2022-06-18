#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

#define BIN_NAME "/challenge/embryoio_level83"

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
            char *argv[50];
            char *envp[2];

            argv[0] = BIN_NAME;

            for (register int i = 1; i < 49; ++i) argv[i] = "garbage";

            argv[49] = "cexocilnpe";

            envp[0] = "243=tyhkwhnwru";
            envp[1] = NULL;

            execve(argv[0], argv, envp);

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
