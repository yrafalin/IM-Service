#!/usr/bin/env python3
import socket, os, threading, string

__version__ = '1.0'
__author__ = 'Yoav Rafalin'

KEY = 568461
EXIT = threading.Event()

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


def send_message(message_to_send, connection, key=True, lenoflenofmsg=5):
    if key is False:
        message = str(message_to_send).encode()
    else:
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


def prelines(serverconnect):
    pass


def displines(serverconnect, displayconnect):
    msg = recv_message(serverconnect)
    send_message(msg, displayconnect, key=False)


def userhost(serverconnect):
    send_message(socket.gethostname(), serverconnect, lenoflenofmsg=3)
    correct = 0
    print('Username must be 10 or less characters.')
    while not correct:
        msg = input('What is your username: ')
        if len(msg) > 10 or len(msg) == 0:
            print('Username must be 10 characters or less.')
            continue
        send_message(msg, serverconnect, lenoflenofmsg=2)
        correct = int(serverconnect.recv(1).decode('utf-8'))
        if not correct:
            print('Someone has that username.')


def typing(serverconnect, displayconnect):
    try:
        while True:
            msg = str(input(': '))
            only_w = []
            for char in msg:
                only_w.append('True' if char in string.whitespace else 'False')
            only_w = eval(' and '.join(only_w))
            if only_w:
                continue
            #if eval(' and '.join(lambda: for x in msg: return True if x in string.whitespace else return False)):
            #    continue
            if msg[:4:] == 'exec':
                msg = msg[4::]
            if msg == 'exit':
                EXIT.set()
                send_message('exec raise SystemExit', displayconnect, key=False)
                print('"Thanks for using my ting!" - Yoav')
                todisplay.close()
                serverconnect.close()
                raise SystemExit
            else:
                send_message(msg.encode().decode('utf-8'), serverconnect)
    except Exception as e:
        if not EXIT.is_set():
            print('Error in typing function', e)
            print('Connection interrupted or broken. Server may be under maintenance.')
            todisplay.close()
            serverconnect.close()
            raise SystemExit


def serverhear(serverconnect, displayconnect):
    try:
        while True:
            msg = recv_message(serverconnect)
            if msg[:4] == 'exec':
                exec(msg[5:])
            else:
                send_message(msg, displayconnect, key=False)
    except Exception as e:
        if not EXIT.is_set():
            print('Error in serverhear function', e)
            print('Connection interuppted or broken. Server may be under maintenance.')
            raise SystemExit


try:
    ip = '127.0.0.1'
    port = 7500
    toserver = socket.socket()
    toserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#To not get Errno [48] port in use
    toserver.connect((ip, port))
except Exception as e:
    print('It looks like you aren\'t on WiFi or the server is under maintenance.')
    print(e)
    raise SystemExit

#Security
#lenofmsg = int(toserver.recv(5).decode('utf-8'))
#msg = decode_with_key(toserver.recv(lenofmsg))
#if msg[:4] == 'exec':
    #exec(msg[5:])

prelines(toserver)

ip = '127.0.0.1'
port = 7501
connect = socket.socket()
connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#To not get Errno [48] port in use
connect.bind((ip, port))
connect.listen(1)

userhost(toserver)

pathtodir = os.path.dirname(os.path.abspath(__file__))
os.system("osascript -e \'tell application \"Terminal\" to do script \"python3 {path}/{version}IMDisplay.py\"\'".format(path=pathtodir, version=__version__.replace('.', ',')))
todisplay, addr = connect.accept()

displines(toserver, todisplay)
talktodisp = threading.Thread(target=serverhear, args=(toserver, todisplay))
talktoserv = threading.Thread(target=typing, args=(toserver, todisplay), daemon=True)
talktodisp.start()
talktoserv.start()
#typing([toserver, todisplay])
#EXIT.wait()
