#!/usr/bin/env python3
#THE LIFESAVER: ^Z then pkill -f name-of-the-python-script
import socket, random, copy, threading, os

__version__ = '1.0'
__author__ = 'Yoav Rafalin'

KEY = 568461
COLOR_CODES = {'blue': '0;34;48', 'green': '0;32;48', 'red': '0;31;48', 'purple': '0;35;48', 'grey': '0;37;48', 'yellow': '0;33;48', 'turquoise': '0;36;48'}
OFF = threading.Event()
CHAT_RECORD = os.path.dirname(os.path.abspath(__file__)) + '/ChatRecords.txt'

def encode_with_key(string):  #Encrypting and decrypting
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


def send_message(message_to_send, connection, lenoflenofmsg=5):
    message = encode_with_key(str(message_to_send))
    length_of_msg = str(len(message))
    length_of_msg = ('0' * (lenoflenofmsg-len(length_of_msg))) + length_of_msg  # This part is adding zeros as padding so that it is always 5 chars
    connection.send(length_of_msg.encode())
    connection.send(message)
    return message, length_of_msg


def recv_message(connection, lenoflenofmsg=5):
    length_of_msg = int(connection.recv(lenoflenofmsg).decode('utf-8'))
    message = decode_with_key(connection.recv(length_of_msg))
    return message


def user_in_string(to_check, list_of_sorts):
    for word in list_of_sorts:
        if word in to_check[:len(word)]:
            return word
    return False


def announce(what, who):
    if type(who) is dict:
        for person in who:
            send_message(what, who[person]['socket'])
    elif type(who) is list:
        for person in who:
            send_message(what, person['socket'])
    else:
        send_message(what, who['socket'])


def record(what, where):
    with open(where, 'a') as black_box:
        black_box.write(what + '\n')


#class clientclass():
#    def __init__(self, ip, hostname, socket, username, thread):
#        self.ip = ip
#        self.hostname = hostname
#        self.socket = socket
#        self.username = username
#        self.thread = thread


def recvandsend(username):
    print(username, 'started')
    global dictofaddr
    data = threading.local()
    try:
        data.msg = '''exec print('Designed and written by Yoav in Python')\ntime.sleep(1)\nprint(\'\'\'Type "help" for commands, "info" for who is on, and "disclaimer" for those of you who don't have more interesting things to do with your lives\'\'\')\nprint('Messages sent will be displayed here:')'''
        send_message(data.msg, dictofaddr[username]['socket'])  # displines function
        data.msg = '{hostname}: {ip} has joined as {username}!'.format(ip=dictofaddr[username]['ip'], hostname=dictofaddr[username]['hostname'], username=username)
        record(data.msg, CHAT_RECORD)
        announce(data.msg, dictofaddr)
        while True:
            data.msg = recv_message(dictofaddr[username]['socket'])
            if data.msg == '/cmd exitall':
                OFF.set()
                raise SystemExit
            elif data.msg[:9] == '/cmd kill':
                if user_in_string(data.msg[10:], dictofaddr):
                    send_message('exec print("Bye Bye, you have been kicked off the server")\nraise SystemExit', dictofaddr[user_in_string(data.msg[10:], dictofaddr)]['socket'])
                    del dictofaddr[user_in_string(data.msg[10:], dictofaddr)]
                    record(username + ': ' + data.msg, CHAT_RECORD)
            elif data.msg == 'info':
                data.msg = '\n'
                for person in dictofaddr:
                    data.msg += '{ip}: {hostname} is online as {username}\n'.format(ip=dictofaddr[person]['ip'], hostname=dictofaddr[person]['hostname'], username=person)
                send_message(data.msg, dictofaddr[username]['socket'])
            elif data.msg == 'disclaimer':
                data.msg = '''\nDisclaimer: I do not intend for this to be used in school.\nI will not be held responsible for anyone who misuses this.\nSince the intent of this is not be used at school,\n'''\
                '''I cannot and will not be held responsible for any punishment or suspension.\nI cannot and will not be punished or suspended for anything related even in the slightest to this program.\n'''\
                '''If you are using this program you agree to these terms and conditions\nAnd please be aware that all __public__ messages are recorded\n*small print goes here*'''
                send_message(data.msg, dictofaddr[username]['socket'])
            elif data.msg == 'help':
                data.msg = '''\nMessages that are sent will appear in THIS window\nTo send a message: Type in the box that you originally ran the program in\nTo send a private message: Type a '/', then (not seperated by a space) the username of the person, and then the message\n'''\
                '''To see who is online: Type 'info'\nTo exit: Type 'exit'\nTo send a colorful message: Type 'color', then the color (options are purple, red, blue, green, yellow, and grey), and then your message\n'''\
                '''To read the disclaimer: Type 'disclaimer'\nBTW available colors are blue, green, red, purple, grey, yellow, and turquoise'''
                send_message(data.msg, dictofaddr[username]['socket'])
            elif data.msg == 'exit':
                send_message('"To infinity and beyond!"', dictofaddr[username]['socket'])
                record(username + ': ' + data.msg, CHAT_RECORD)
                raise Exception
            elif data.msg[:5] == 'color':
                if user_in_string(data.msg[6:], COLOR_CODES):
                    data.msg = '\x1b[{}m'.format(COLOR_CODES[user_in_string(data.msg[6:], COLOR_CODES)]) + username + ': ' + data.msg[len(user_in_string(data.msg[6:], COLOR_CODES)) + 7:] + '\x1b[0m'
                    print(data.msg)
                    announce(data.msg, dictofaddr)
                    record(data.msg, CHAT_RECORD)
            elif data.msg[:1] == '/':
                if user_in_string(data.msg[1:], dictofaddr):
                    data.userto = user_in_string(data.msg[1:], dictofaddr)
                    data.msg = 'PM from ' + username + ': ' + data.msg[2 + len(data.userto):]
                    send_message(data.msg, dictofaddr[data.userto]['socket'])
                    record('{username}: PM to {userto}'.format(username=username, userto=data.userto), CHAT_RECORD)
                else:
                    send_message('No comprendo wat u sed', dictofaddr[username]['socket'])
            else:
                data.msg = username + ': ' + data.msg
                print(data.msg)
                record(data.msg, CHAT_RECORD)
                announce(data.msg, dictofaddr)
    except KeyboardInterrupt:
        OFF.set()
        raise SystemExit
    except Exception as e:
        if username in dictofaddr:
            print(dictofaddr)
            print('e', e)
            tmp = dictofaddr[username]
            del dictofaddr[username]
            announce('{username}: {hostname} has left\n'.format(username=username, hostname=tmp['hostname']), dictofaddr)


def acceptnew():
    ip = '127.0.0.1'
    #ip = '192.168.7.226'
    port = 7500
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#To not get Errno [48] port in use
    connection.bind((ip, port))
    connection.listen(1)
    global dictofaddr
    while True:
        try:
            user = None
            server, addr = connection.accept()
            #Security
            #POSSIBLE LOCATION SECURITY: location = subprocess.check_output([\'curl\', \'freegeoip.net/csv/\']).decode(\'utf-8\').split(\',\')\nif location[2] != \'US\':\n   raise SystemExit
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
            host = decode_with_key(server.recv(lenofmsg))
            #Username
            round1 = True
            while user_in_string(user, dictofaddr) or round1 == True:
                round1 = False
                lenofmsg = int(server.recv(2).decode('utf-8'))
                user = decode_with_key(server.recv(lenofmsg))
                print(user)
                if user not in dictofaddr:
                    server.send('1'.encode())
                else:
                    server.send('0'.encode())
                print('checked')
            print('accepted')

            newthread = threading.Thread(target=recvandsend, args=(user, ), daemon=True)
            print(dictofaddr)
            dictofaddr[user] = {'ip': addr, 'hostname': host, 'socket': server, 'thread': newthread}#clientclass(addr, host, server, user, newthread)#{ip: addr, hostname: host, socket: server, username: user, thread: newthread}
            print('about to start newthread')
            newthread.start()
            newthread = None
        except KeyboardInterrupt:
            raise SystemExit
        except Exception as e:
            if user in dictofaddr:
                print(dictofaddr)
                print(e)
                del dictofaddr[user]
                print(dictofaddr)


#ip = '127.0.0.1'
#ip = '192.168.7.226'
#port = 7500
#connect = socket.socket()
#connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#To not get Errno [48] port in use
#connect.bind((ip, port))
#connect.listen(1)
dictofaddr = {}
#acceptnew()
acceptem = threading.Thread(target=acceptnew, daemon=True)
acceptem.start()
OFF.wait()
