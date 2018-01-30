#!/usr/bin/env python3
import socket,  time

__version__ = '1.0'
__author__ = 'Yoav Rafalin'

ip = '127.0.0.1'
port = 7501
toeditor = socket.socket()
toeditor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#To not get Errno [48] port in use
try:
    toeditor.connect((ip, port))
except:
    print('To connect to the chat, type into the Terminal app "python3 IMEditor.py" from the folder it is in and press enter OR type "python3 " and then drag in the Python file from Finder.')
    raise SystemExit

try:
    print()
    while True:
        lenofmsg = int(toeditor.recv(5).decode('utf-8'))
        msg = toeditor.recv(lenofmsg).decode('utf-8')
        if msg[:4] == 'exec':
            exec(msg[5:])
        else:
            print(msg)
except SystemExit:
    print('"Thanks for using my ting!" - Yoav')
except:
    print('\nLooks like something was closed!')
    print('Try to run IMEditor.py again.')
