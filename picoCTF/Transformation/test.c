#include <stdio.h>
#include <string.h>

int
main(void)
{
    FILE *ptr = fopen("./enc", "r");

    fputs("%d\n", ptr);
    
    return 0;
}
