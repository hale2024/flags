open the capture.pcap in wireshark, right-click on one of the captures and click
on follow tcp stream, it will show you the entire conversation the user had.
Now the characters in the password are like so "backdoor...00Rm8.ate". If viewed
in hex, those dots are actually the character "0x7f" which is delete in ASCII.
Hence, the password is "backd00Rmate".
