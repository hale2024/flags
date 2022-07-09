/* Connects to the remote IP given the address and port */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>

#define NODE "localhost"
#define SERVICE "1414"

/* return the sockaddr: inet or inet6 */
void* get_addr_in(struct sockaddr *);

/* for reading and writing to the server */
void pwncollege(int);

int main(int argc, char *argv[]) {
    /* hints for getaddrinfo() */
    struct addrinfo hints;
    /* to store the results from getaddrinfo() */
    struct addrinfo *remote_addr;
    /* status code from getaddrinfo() */
    int status;
    /* to loop over the linked list of remote_addr */
    struct addrinfo *p;
    /* socket file descriptor */
    int sockfd;

    memset(&hints, '\0', sizeof hints);
    hints.ai_family = AF_UNSPEC; // can be IPv4 or IPv6
    hints.ai_socktype = SOCK_STREAM;

    if ( (status = getaddrinfo(NODE, SERVICE, &hints, &remote_addr)) != 0 ) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(status));
        return EXIT_FAILURE;
    }

    for (p = remote_addr; p != NULL; p = p->ai_next) {

        /* open the socket */
        if ( (sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
            perror("socket");
            fprintf(stderr, "socket: trying the next address\n");
            continue;
        }

        /* connect to the remote */
        if ( connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
            close(sockfd);
            perror("connect");
            fprintf(stderr, "connect: trying the next address\n");
            continue;
        }

        break;
    }

    if (p == NULL) {
        fprintf(stderr, "client: failed to connect\n");
        return EXIT_FAILURE;
    }

    freeaddrinfo(remote_addr);

    /* this will do the reading and writing */
    pwncollege(sockfd);

    close(sockfd);

    return EXIT_SUCCESS;
}

void* get_addr_in(struct sockaddr *sa) {
    if (sa->sa_family == AF_INET) {
        return &( ((struct sockaddr_in *)sa)->sin_addr );
    }
    return &( ((struct sockaddr_in6 *)sa)->sin6_addr );
}

void pwncollege(int sock) {
    char buf[BUFSIZ];
    int n;

    for ( ;; ) {
        explicit_bzero(buf, sizeof(buf));

        /* read the message from the server */
        read(sock, buf, sizeof(buf));
        printf("%s", buf);

        explicit_bzero(buf, sizeof(buf));
        n = 0;

        /* read input from console */
        while ( (buf[n++] = getchar()) != '\n' );

        /* If the input string is long enough and is other than just a newline,
         * then send that to the server */
        if ( (strlen(buf) > 1) && strcmp(buf, "\n") ) {
            write(sock, buf, strlen(buf));
        }
    }

    return;
}
