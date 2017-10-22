#!/usr/bin/env python
import socket, os, time

ip = '127.0.0.1'
port = 7500
toeditor = socket.socket()
toeditor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#To not get Errno [48] port in use
while True:
    try:
        toeditor.connect((ip, port))
        break
    except:
        time.sleep(0.2)

#print('Disclaimer: I do not intend for this to be used in school.')
#print('I will not be held responsible for anyone who misuses this.')
#print('Since the intent of this is not be used at school,')
#print('I cannot and will not be held responsible for any punishment or suspension.')
#print('I cannot and will not be punished or suspended for anything related even in the slightest to this program.')

try:
    print('Designed and written by Yoav in Python')
    time.sleep(1)
    print('With emotional support from Akshar')
    time.sleep(1)
    print('And other contributions by Colin S.')
    time.sleep(1)
    print('Type "help" for commands, "info" for who is on, and "disclaimer" for those of you who don\'t have more interesting things to do with your lives')
    print('Messages sent will be displayed here:')
    while True:
        lenofmsg = int(toeditor.recv(5).decode('utf-8'))
        print(toeditor.recv(lenofmsg).decode('utf-8'))
except Exception as e:
    print(e)
    print('\nLooks like you closed something!')
    print('Try to run the editor again.')
