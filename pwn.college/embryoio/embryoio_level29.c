#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

#define BIN_NAME "/challenge/embryoio_level29"

void pwncollege(void) { return; }

int main(void)
{
    pid_t pid = fork();

    switch (pid)
    {
        case -1:
        {
            perror("fork()");
            _exit(EXIT_FAILURE);
            break;
        }
        case 0:
        {
            /* we are the child process so exec the binary */
            char *argv[2] = {BIN_NAME, NULL};
            char *envp[1] = {NULL};
            execve(argv[0], argv, envp);
            /* exec() never returns so it must have failed */
            _exit(EXIT_FAILURE);
            break;
        }
        default:
        {
            /* wait for the child since we're the parent */
            waitpid(pid, NULL, 0);
            break;
        }
    }
    return EXIT_SUCCESS;
}
