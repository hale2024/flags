/* This challenge takes input over file descriptor 206 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>

#define BIN_NAME  "/challenge/embryoio_level94"

int main(void)
{
    int fd2;
    pid_t pid;

    /* duplicate stdin's fd to be 206 */
    fd2 = 206;

    if ( dup2(STDIN_FILENO, fd2) == -1) {
        perror("dup2()");
        _exit(EXIT_FAILURE);
    }

    char *argv[3] = {BIN_NAME, NULL};
    execve(argv[0], argv, NULL);

    return EXIT_SUCCESS;
}
