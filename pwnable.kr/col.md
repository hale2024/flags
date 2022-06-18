* Our input needs to be 20 bytes which will all be converted to 5 chunks each of 4
bytes.
* Each of the bytes sum needs to result 0x21DD09EC.
* Let's suppose our first 16 bytes are 0x01, then:
    hex(0x21DD09EC - 0x04040404) = 0x1dd905e8
* So giving 0x1dd905e8 + 16 * 0x01 should result in required sum
    ./col "$(python -c 'print "\x01"*16 + "\xe8\x05\xd9\x1d"')"
* I don't know why but
    hex(0x21DD09EC - 0x01010101) = 0x20dc08eb
doesn't work, the 0x01 needs to be 0x04 when checking result but the input
should still be 0x01
