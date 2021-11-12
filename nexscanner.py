#!/usr/bin/python3
import requests
from threading import Thread, Lock
from queue import Queue
import sys


# For the wordlist
queue_list = Queue()
lock_list = Lock()
success_list = list()

# colors
whi = "\033[1;37m"
pur = "\033[1;35m"
red = "\033[1;31m"
gre = "\033[0;32m"
yel = "\033[1;33m"
ye = "\033[0;33m"
cya = "\033[0;36m"
blu = "\033[1;34m"
res = "\033[0;37;40m"

def print_banner():
    print(f"{cya}  _    _             _____   	 	   ")
    print(f" | |\ | |           |  ___|			       ")
    print(f" | | \| | ______  __| |___ ________________")
    print(f" | |\   |/  _ \ \/ /|____ | __/|    |  __ |")
    print(f" | | \  |  ___/>  <  ___| | |__| -  | | | |")
    print(f" |_|  \_|\____/_/\_\|_____|\__/|___ |_| |_|")
    print(f"\t\t\t{gre}NexScanner v1.0{cya}")
    print(f"{gre}[{whi}-{gre}]Author: Anonymous Hacks")
    print(f"{gre}[{whi}-{gre}]GitHub: https://github.com/4anonz")


def find_admin_panel(url, n):
    global queue_list, success_list, lock_list
    try:
        while True:
            admin = queue_list.get()
            
            tmp_url = url + admin
            try:
                if n == 1:
                    sys.stdout.write(f"{pur}[{whi}*{pur}]{ye} Trying {admin} {whi}==> {res}")
                req = requests.get(tmp_url, timeout=5, allow_redirects=False)
                # If the response code is 200
                # Then it means the current url it is correct
                if req.status_code == 200:
                    with lock_list:
                        success_list.append(admin)
                    if n == 1:
                        sys.stdout.write(f"{yel}Found\n")
                    else:
                        print(f"{pur}[{whi}*{pur}]{ye} Found {tmp_url}")
                    sys.stdout.flush()
                    queue_list.task_done()
                    continue
                else:
                    queue_list.task_done()
                    if n == 1:
                        sys.stdout.write(f"{red}Not Found\n")
                    sys.stdout.flush()
            except Exception as err:
                print(err)
    except KeyboardInterrupt:
        print(f"\n{pur}[{whi}*{pur}]{ye} CTRL+C Quitting!!")
        exit(0)


def scan_subdomain(url, protocol):
    global success_list, queue_list
    try:
        while True:
            sub = queue_list.get()
            tmp_url = f"{protocol}{sub}.{url}"
            try:

                req = requests.get(tmp_url)
            except requests.ConnectionError:
                pass
            except Exception as err:
                print(err)

            else:
                print(f"{pur}[{whi}*{pur}]{ye} Found {tmp_url}")
                with lock_list:
                    success_list.append(tmp_url)
                queue_list.task_done()
    except KeyboardInterrupt:
        print(f"\n{pur}[{whi}*{pur}]{ye} CTRL+C Quitting!!")
        exit(0)


if __name__ == '__main__':

    try:

        print_banner()
        print(f"""
{red}[{yel}01{red}]{cya} Admin Panel Finder
{red}[{yel}02{red}]{cya} Sub-Domain Scanner
{red}[{yel}00{red}]{cya} Exit
        """)

        print(f"{blu}┌──({whi}NexScanner{blu})-[~{ye}Enter your choice{blu}]")
        choice = str(input(f"└─${res} "))
        # Check the user's choice
        if choice == '01' or choice == '1':
            choice = '1'
        elif choice == '02' or choice == '2':
            choice = 2
        else:
            exit(0)
        
        print(f"{ye}Enter a complete URL of the site. example: {gre}http://127.0.0.1")
        print(f"{blu}┌──({whi}NexScanner{blu})-[~{ye}Enter URL{blu}]")
        url = str(input(f"└─${res} "))


        try:
            print(f"{ye}Press {whi}CTRL+C{ye} if you want to use default wordlist\nOtherwise provide a wordlist")
            print(f"{blu}┌──({whi}NexScanner{blu})-[~{ye}Wordlist{blu}]")
            wordlist = str(input(f"└─${res} "))
        except KeyboardInterrupt:
            if choice == '1':
                wordlist = "admin.txt"
            else:
                wordlist = "subdomains.txt"
        
        
        try:
            # Read the wordlist file
            # and add each to the queue list
            with open(wordlist, "rb") as words:
                for last_in_list in words:
                    queue_list.put(last_in_list.strip().decode())
        except FileNotFoundError:
            print(f"{red}[{whi}-{red}]{ye} Wordlist file not found!")
            exit(1)
        
        try:
            print(f"{ye}Press {whi}CTRL+C{ye} if you don't want to use threads")
            print(f"{blu}┌──({whi}NexScanner{blu})-[~{ye}Number of threads{blu}]")
            threads_num = int(input(f"└─${res} "))
        except KeyboardInterrupt:
            threads_num = 1
        except ValueError:
            print(f"{red}[{whi}-{red}]{ye} Error expecting an integer value here!")
            exit(1)
        
        # Add a forward slash if the user doesn't include it
        if not url.endswith("/"):
                url = url + "/"
        print(f"{pur}[{whi}*{pur}]{ye} Trying.. hold on\press CTRL+C to quit")
        if choice == '1':
            for i in range(threads_num):
                thread = Thread(target=find_admin_panel, args=(url, threads_num, ))
                # A deamon thread
                thread.deamon = True
                thread.start()
        else:
            if "https://" in url:
                url = url.replace("https://", "")
                protocol = "https://"
            elif "http://" in url:
                url = url.replace("http://", "")
                protocol = "https://"
            for i in range(threads_num):
                thread = Thread(target=scan_subdomain, args=(url, protocol,))
                thread.deamon = True
                thread.start()
    except KeyboardInterrupt:
        print(f"\n{pur}[{whi}*{pur}]{ye} CTRL+C Quitting!!")
        exit(0)
