#!/usr/bin/env python3

import socket
import pickle

#Define the server host and port
HOST = '127.0.0.1'
PORT = 65432

#menu A
print("hiii")
mA = 0
while mA!=1 and mA!=2:
    mA = int(input("Enter \n1 for Record Creation\n2 for Record Retrieval"))
    print(mA)

#if 1 chosen, Record Input
#user input for records/rows
if mA==1:
    inName = input("Name:")
    inID = input("ID:")
    inStNum = input("Street Number: ")
    inStName = input("Street Name: ")
    inCity = input("City: ")
    inPost = input("Postal Code: ")
    inProv = input("Province")
    inCountry = input("Country: ")

    infoSend = [inName, inID, inStNum, inStName, inCity, inPost, inProv, inCountry]

    dataSend = pickle.dumps(infoSend)
#if 2 chosen, Record ID input

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))
    s.sendall(dataSend)
    data = pickle.loads(s.recv(1024))

print('recieved', repr(data))
