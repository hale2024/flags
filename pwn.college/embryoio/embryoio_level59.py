import subprocess


challenge_binary = "/challenge/embryoio_level59";


p1 = subprocess.Popen("/usr/bin/rev", stdout=subprocess.PIPE);
p2 = subprocess.Popen(challenge_binary, stdin=p1.stdout);

p1.wait();
