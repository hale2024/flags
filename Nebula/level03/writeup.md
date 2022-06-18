since we can basically put any file and it will get executed as `flag03`, we can
make it compile a C program and set that compiled program as uid so that when we
execute it the suid will be that of `flag03`. The C program basically executes
`/bin/sh` after setting the uid to 996 (flag03).
