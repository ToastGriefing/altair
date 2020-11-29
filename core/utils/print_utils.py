import colorama, random, re

from colorama import *

colorama.init()

def parse_string(string):
    return re.sub(r'§[a-zA-Z0-9]|&[a-zA-Z0-9]', '', string)

def remove_colors_from_string(string):
    colors = [Fore.BLACK, Fore.BLUE, Fore.CYAN, Fore.WHITE, Fore.GREEN, Fore.MAGENTA, Fore.YELLOW, Fore.RED, Style.BRIGHT, Style.DIM, Style.NORMAL]
    for color in colors:
        string = string.replace(color, '')
    return string

def print_banner():
    banners = [
    f'''{Fore.WHITE}
      
{Fore.WHITE}*{Fore.CYAN}={Fore.BLUE}-_ {Fore.WHITE}╔-╗ ╔╦╗ ╦   ╔-╗ + ╦-╗ {Fore.BLUE}_-{Fore.CYAN}={Fore.WHITE}*
{Fore.WHITE}*{Fore.CYAN}={Fore.BLUE}-_ {Fore.WHITE}╠-╣  /  /   ╠-╣ / ╠╦╝ {Fore.BLUE}_-{Fore.CYAN}={Fore.WHITE}*
{Fore.WHITE}*{Fore.CYAN}={Fore.BLUE}-_ {Fore.WHITE}╩ ╩  ╩  ╩-╝ ╩ ╩ ╩ ╩╚- {Fore.BLUE}_-{Fore.CYAN}={Fore.WHITE}*
   {Fore.BLUE}`[{Fore.WHITE} minecraft rcon tool {Fore.BLUE}]'{Fore.WHITE}
       {Fore.RED}`{Fore.WHITE}by t.me/wejdene{Fore.RED}`{Fore.WHITE}    
    ''',
    f'''{Fore.WHITE}
     _ _             
 ___| | |_ ___ _ ___
| .'| |  _| .'| |  _| {Fore.CYAN}'{Fore.WHITE}made by toastz{Fore.CYAN}'{Fore.YELLOW}
|__,|_|_| |__,|_|_|   {Fore.CYAN}`{Fore.WHITE}c00l rcon t00l{Fore.CYAN}`{Fore.WHITE}
    ''',
    f'''
            {Fore.CYAN} _____
          {Fore.GREEN}.-'.  ':'{Fore.CYAN}-.   {Fore.WHITE}  RCON TOOLZ
        {Fore.GREEN}.''::: .:    {Fore.CYAN}'. {Fore.WHITE}  BY ITSTOASTZ
      {Fore.CYAN} /   {Fore.GREEN}:::::'    {Fore.CYAN}  \\  {Fore.RED}        _ _        _      
      {Fore.CYAN};.   {Fore.GREEN} ':' `    {Fore.CYAN}   ;  {Fore.RED}  __ _| | |_ __ _(_)_ __ 
      {Fore.CYAN}|    {Fore.GREEN}   '..    {Fore.CYAN}   |  {Fore.RED} / _` | | __/ _` | | '__|
      {Fore.CYAN}; '  {Fore.GREEN}    ::::. {Fore.CYAN}   ;  {Fore.RED}| (_| | | || (_| | | |
      {Fore.CYAN} \   {Fore.GREEN}    ':::: {Fore.CYAN}  /   {Fore.RED} \__,_|_|\__\__,_|_|_| 
      {Fore.CYAN}  '. {Fore.GREEN}     :::  {Fore.CYAN}.'
      {Fore.CYAN}    '-.___{Fore.GREEN}'{Fore.CYAN}_.-'
{Fore.WHITE}
    '''



    ]



    print(random.choice(banners))

def clear_console():
    print("\x1b[2J")
    print_banner()

def print_success(msg):
    print(f'{Fore.GREEN}[+]{Fore.WHITE} {msg}')

def print_failed(msg):
    print(f'{Fore.RED}[-]{Fore.WHITE} {msg}')

def print_error(msg):
    print(f'{Fore.YELLOW}[!]{Fore.WHITE} {msg}')

def print_loading(msg):
    print(f'{Fore.CYAN}[*]{Fore.WHITE} {msg}')


def draw_string(string, color=Fore.CYAN):
    final_string = ''

    # key:value json
    if type(string) == dict:

        max_1 = 0
        max_2 = 0

        for v1, v2 in string.items():
            v1 = str(v1)
            v2 = str(v2)

            if len(v1) > max_1:
                max_1 = len(v1)
            elif len(v2) > max_2:
                max_2 = len(v2)

        final_string = ''
        final_string += color + '╔═' + ('═' * max_1) + '═╦═' + ('═' * max_2) + '═╗' + '\n'

        for v1, v2 in string.items():
            v1 = str(v1)
            v2 = str(v2)
            final_string += color + '║ ' + Fore.WHITE + v1 + (' ' * (max_1 - len(v1))) + color + ' ║ ' + Fore.WHITE + v2 + (' ' * (max_2 - len(v2))) + color + ' ║\n'
        final_string += color + '╚═' + ('═' * max_1) + '═╩═' + ('═' * max_2) + '═╝'
        print(final_string)
        return

    elif type(string) == str:

        # simple string
        if not '\n' in string:
            final_string += color + '╔═' + '═' * len(string) + '═╗\n' + '║ ' + Fore.WHITE + string + color + ' ║\n' + '╚═' + '═' * len(string) + '═╝'
            print(final_string + Fore.WHITE)
            return

        # string with \n
        max_lenght = 0
        lines = string.split('\n')
        for line in lines:
            if len(line) > max_lenght:
                max_lenght = len(line)
    
        final_string += color + '╔═' + '═' * max_lenght + '═╗\n'
        for line in lines:
            final_string += color + '║ ' + Fore.WHITE + line + ' ' * (max_lenght - len(line)) + color + ' ║\n'
        final_string += color + '╚═' + '═' * max_lenght + '═╝'
        print(final_string + Fore.WHITE)
        return

