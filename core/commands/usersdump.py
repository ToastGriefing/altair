import socket, struct, hashlib, colorama, uuid, re

from colorama import *
from core.utils.packet_utils import *
from core.utils.print_utils import *

colorama.init()

def userdump(s):
    player_list = ''
    packet = command_packet('ebaltop 1')
    s.sendall(packet)
    data = parse_string(s.recv(65500).decode('utf-8', errors='ignore'))
    if len(data.split('\n')) > 3:
        print_loading('getting users list...')
        page_number = int(re.findall(r'\ \d+/(\d+)\ [\-]+', data)[0])
        for page in range(page_number + 1):
            packet = command_packet('ebaltop ' + str(page))
            s.sendall(packet)
            data = parse_string(s.recv(65500).decode('utf-8', errors='ignore'))
            try:
                players = re.findall(r'\d+\.\ (\w+),\ ', data)
                for player in players:
                    if not player in str(player_list):
                        player_list += f'{player}\n'
            except:
                pass
        

        with open(f'{s.getpeername()[0]}.players.txt', 'a+') as f:
            f.write(f'# players dumped w/Altair (@ToastGriefing on telegram)\n{player_list}')
        print_success(f'players list have been saved @ \'{s.getpeername()[0]}.players.txt\'')
    else:
        print_error('there was an error, please run the command again!')    