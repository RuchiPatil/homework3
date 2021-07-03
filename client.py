#!/usr/bin/env python3
#------------------------------LIBRARIES
import socket
import pickle
import yaml
import re
import pandas as pd
#----------------------------GLOBAL VALUES
HOST = '127.0.0.1'
PORT = 65432
cols = ['Name', 'ID', 'StreetNumber', 'StreetName', 'City', 'Province', 'Country']
#---------------------------------------------------------------------------------------MENU

mA = 0
while True:
    mA = input("Enter \n1 for Record Creation\n2 for Record Retrieval\n")
    if mA=='1' or mA=='2':
        break
    print("             You can only choose 1 or 2! :)")
mA = int(mA)
#if 1 chosen, Record Input
datasend = [[], 0] #1 means data is record, 2 means data is ID

#------------------------------------------------------------------------ (if 1) RECORD INPUT
if mA==1:
    print("\n⁛⁛⁛⁛1. Create record⁛⁛⁛⁛\n")
    #-------------- Name - check alpha
    while True:
        inName = input('Name: ')
        if inName.isalpha():
            break
        print("             ERR: letters, please :)")
    #-------------- ID - check len=6, digit
    while True:
        inID = input("ID: ")
        if inID.isdigit() and len(inID)==6:
            break
        print("             ERR: 6-digit ID, please :)")
    #-------------- StNum - check len <=4, digit
    while True:
        inStNum = input("Street Number: ")
        if inStNum.isdigit() and len(inStNum)<=4:
            break
        print("             ERR: upto 4 digits, please :)")
    #-------------- St Name
    inStName = input("Street Name: ")
    #-------------- City - check alpha
    inCity = input("City: ")
    #-------------- Postal Code - check re zip format
    zipc = re.compile(r"\w\d\w\s\d\w\d")
    while True:
        inPost = input('Enter Postal Code (A1A 1A1): ')
        if zipc.match(inPost):
            break
        print("             ERR: 'A1A 1A1' formatting, please :)")
    #-------------- Province
    inProv = input("Province: ")
    #-------------- Country - check alpha
    while True:
        inCountry = input('Country: ')
        if inCountry.isalpha():
            break
        print("             ERR: only letters, please :)")

    infoSend = [inName, inID, inStNum, inStName, inCity, inPost, inProv, inCountry]
    #LIST TO BYTES
    dataSend = bytes(str([infoSend, 1]), 'UTF-8')

##------------------------------------------------------------------------ (if 2) ID INPUT
elif mA==2:
    print("\n⁛⁛⁛⁛2. Retrieve record⁛⁛⁛⁛\n")
    while True:
        retid = input("Retrieval ID: ")
        if retid.isdigit() and len(retid)==6:
            break
        print("             ERR: 6-digit ID, please :)")
    #STR TO BYTES
    dataSend = bytes(str([retid, 2]), 'UTF-8')

#----------------------------------------------------------------------------SOCKET CONNECT
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))
    s.sendall(dataSend)
    #BYTES TO STRING
    dataR = (s.recv(1024)).decode('UTF-8')
# ----------------------------------------------------------------------------Print Received Data
retframe = pd.DataFrame(columns= ['Name', 'ID', 'StreetNumber', 'StreetName', 'City', 'Province', 'Country'])
if mA==2:
    dataR = yaml.safe_load(dataR)
    dataR.insert(0, cols)
    #retframe = pd.DataFrame(dataR, columns=cols)
    retframe = pd.DataFrame.from_records(dataR)
    #retframe.axis('off')
    #retframe.columns = ['Name', 'ID', 'StreetNumber', 'StreetName', 'City', 'Province', 'Country']
    print(retframe)
else:
    print('recieved', repr(dataR))
