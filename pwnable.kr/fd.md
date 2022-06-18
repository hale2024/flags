* 0x1234 is subtracted from our input
* we need the program to read from stdout
  whose fd is 0
* so to make the program's fd be 0, we need atoi( argv[1] ) - 0x1234 to be 0
* 0x1234 = 4660
* input 4660 as argv[1] and type "LETMEWIN"
