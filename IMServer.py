#!/usr/bin/env python
#THE LIFESAVER: ^Z then pkill -f name-of-the-python-script
import socket, random, copy, threading
from multiprocessing import Process

KEY = 97531
OFF = threading.Event()

def encode_with_key(string):#Encrypting and decrypting
    list_of_numbers = ''
    for letter in string:
        list_of_numbers += str(ord(letter)*KEY) + ' '
    return list_of_numbers.encode()

def decode_with_key(byte):
    string_of_bytes = ''
    list_of_bytes = (byte.decode('utf-8')).split()
    for b in list_of_bytes:
        string_of_bytes += chr(int(int(b)//KEY))
    return string_of_bytes

class clientclass():
    def __init__(self, ip, hostname, socket, username, thread):
        self.ip = ip
        self.hostname = hostname
        self.socket = socket
        self.username = username
        self.thread = thread

def recvandsend(username):
    global dictofaddr
    data = threading.local()
    try:
        data.msg = '{ip}: {hostname} has joined as {username}!'.format(ip=dictofaddr[username].ip, hostname=dictofaddr[username].hostname, username=username)
        data.lenofmsg = str(len(encode_with_key(data.msg)))
        data.lenofmsg = ('0' * (5-len(data.lenofmsg))) + str(data.lenofmsg)
        for address in dictofaddr:
            dictofaddr[address].socket.send(data.lenofmsg.encode())
            dictofaddr[address].socket.send(encode_with_key(data.msg))
        while True:
            data.lenofmsg = int(dictofaddr[username].socket.recv(5).decode('utf-8'))
            data.msg = decode_with_key(dictofaddr[username].socket.recv(data.lenofmsg))
            if data.msg == 'cmd exitall -f':
                OFF.set()
                raise SystemExit
            elif data.msg[:1:] == '/':
                data.msgwords = data.msg.split()
                print('msgwords', data.msgwords)
                data.userto = data.msgwords[0][1:]
                print('userto', data.userto)
                del data.msgwords[0]
                print('msgwords2', data.msgwords)
                data.msg = ''
                for word in data.msgwords:
                    data.msg += word + ' '
                data.msg = 'DM from ' + username + ': ' + data.msg
                print(data.msg)
                data.lenofmsg = str(len(encode_with_key(data.msg)))
                data.lenofmsg = ('0' * (5-len(data.lenofmsg))) + str(data.lenofmsg)
                for address in dictofaddr:
                    if dictofaddr[address].username == data.userto:
                        dictofaddr[address].socket.send(data.lenofmsg.encode())
                        dictofaddr[address].socket.send(encode_with_key(data.msg))
                if OFF.is_set():
                    raise SystemExit
            else:
                data.msg = username + ': ' + data.msg
                print(data.msg)
                data.lenofmsg = str(len(encode_with_key(data.msg)))
                data.lenofmsg = ('0' * (5-len(data.lenofmsg))) + str(data.lenofmsg)
                for address in dictofaddr:
                    dictofaddr[address].socket.send(data.lenofmsg.encode())
                    dictofaddr[address].socket.send(encode_with_key(data.msg))
                if OFF.is_set():
                    raise SystemExit
    except KeyboardInterrupt:
        OFF.set()
        raise SystemExit
    except Exception as e:
        if OFF.is_set():
            raise SystemExit
        if username in dictofaddr:
            print('bye')
            print(dictofaddr)
            print(e)
            del dictofaddr[username]
            print(dictofaddr)

def acceptnew():
    connection = connect
    global dictofaddr
    while True:
        if OFF.is_set():
            raise SystemExit
        try:
            username = None
            server, addr = connection.accept()
            #Security
            #POSSIBLE LOCATION SECURITY: location = subprocess.check_output([\'curl\', \'freegeoip.net/csv/\']).decode(\'utf-8\').split(\',\')\nif location[2] != \'US\':\n   raise SystemExit
            print('security now')
            #security = 'exec pass'
            '''diritems = os.listdir(os.path.dirname(os.path.abspath(__file__)))
            comp = socket.gethostname()
            if len(diritems) != 2 and comp != 'NMB11016-8-yoarafa':
                raise SystemExit
            if __file__ != 'IMEditor.py':
                raise SystemExit
            if 'IMEditor.py' not in diritems or 'IMDisplay.py' not in diritems:
                raise SystemExit'''
            #lenofmsg = str(len(encode_with_key(security)))
            #lenofmsg = ('0' * (5-len(lenofmsg))) + str(lenofmsg)
            #connection.send(lenofmsg.encode())
            #connection.send(encode_with_key(security))
            #Hostname
            lenofmsg = int(server.recv(3).decode('utf-8'))
            hostname = decode_with_key(server.recv(lenofmsg))
            #Username
            round1 = True
            while username in dictofaddr or round1 == True:
                print('start username loop')
                round1 = False
                lenofmsg = int(server.recv(2).decode('utf-8'))
                username = decode_with_key(server.recv(lenofmsg))
                print('resplendant')
                if username not in dictofaddr:
                    server.send('1'.encode())
                else:
                    server.send('0'.encode())
            print('username done. phewww')
            newthread = threading.Thread(target=recvandsend, args=(username,))
            dictofaddr[username] = clientclass(addr, hostname, server, username, newthread)
            newthread.start()
            newthread = None
        except KeyboardInterrupt:
            OFF.set()
            raise SystemExit
        except Exception as e:
            if OFF.is_set():
                raise SystemExit
            if username in dictofaddr:
                print('bye')
                print(dictofaddr)
                print(e)
                del dictofaddr[username]
                print(dictofaddr)


#ip = '127.0.0.1'
ip = '192.168.7.226'
port = 10001
connect = socket.socket()
connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#To not get Errno [48] port in use
connect.bind((ip, port))
connect.listen(1)
dictofaddr = {}
acceptnew()
#acceptem = threading.Thread(target=acceptnew)
#acceptem.start()
#OFF.wait()
#raise SystemExit
