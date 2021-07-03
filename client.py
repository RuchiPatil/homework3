#!/usr/bin/env python3
#------------------------------LIBRARIES
import socket
import pickle
import yaml
#----------------------------GLOBAL VALUES
HOST = '127.0.0.1'
PORT = 65432

#---------------------------------------------------------------------------------------MENU
print("hiii")
mA = 0
while mA!=1 and mA!=2:
    mA = int(input("Enter \n1 for Record Creation\n2 for Record Retrieval"))
    print(mA)

#if 1 chosen, Record Input
datasend = [[], 0] #1 means data is record, 2 means data is ID

#------------------------------------------------------------------------ (if 1) RECORD INPUT
if mA==1:
    inName = input("Name:")
    inID = input("ID:")
    inStNum = input("Street Number: ")
    inStName = input("Street Name: ")
    inCity = input("City: ")
    inPost = input("Postal Code: ")
    inProv = input("Province: ")
    inCountry = input("Country: ")

    infoSend = [inName, inID, inStNum, inStName, inCity, inPost, inProv, inCountry]
    #LIST TO BYTES
    dataSend = bytes(str([infoSend, 1]), 'UTF-8')

##------------------------------------------------------------------------ (if 2) ID INPUT
elif mA==2:
    retid = input("Retrieval ID: ")
    #STR TO BYTES
    dataSend = bytes(str([retid, 2]), 'UTF-8')

#----------------------------------------------------------------------------SOCKET CONNECT
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))
    s.sendall(dataSend)
    #BYTES TO STRING
    dataR = (s.recv(1024)).decode('UTF-8')

if dataSend[1]==2:
    dataR = yaml.safe_load(dataR)
print('recieved', repr(dataR))
