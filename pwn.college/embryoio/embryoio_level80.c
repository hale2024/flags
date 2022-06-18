#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

#define BIN_NAME "/challenge/embryoio_level80"

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
            char *argv[103];

            argv[0] = BIN_NAME;

            for (register int i = 1; i < 101; ++i)
            {
                argv[i] = "never_gonna_give_you_up";
            }

            argv[101] = "slwqlpkoln";
            argv[102] = NULL;

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
