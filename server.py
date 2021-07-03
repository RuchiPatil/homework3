#!/usr/bin/env python3

import socket
import pickle
import yaml
import pandas as pd
import os.path as osp
import csv
#--------------------------------------------------------FUNCTIONS
# FUNC make a csv with fields
def createCSV(filename):
    if osp.isfile(filename):
        return 0
    else:
        #Create empty dataframe with column names
        df = pd.DataFrame(columns= ['Name', 'ID', 'StreetNumber', 'StreetName', 'City', 'Province', 'Country'])
        #export dataframe to csv file
        df.to_csv (filename, index = False, header=True)

#FUNC write to the csv filename
def writeCSV(row, filename):
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row)
        return "Record written!"

#FUNC read from the csv file
def readCSV(retID, filename):
    frame = pd.read_csv(filename)
    retrows = (frame[(frame.ID == retID)]).values.tolist()
    print("retrows:\n", retrows)
    return retrows
#------------------------------------------------------EOF FUNCTIONS
HOST = '0.0.0.0'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    affirm = "we got it"
    with conn:
        print('connected by', addr)
        while True:
            #BYTES to STRING
            recieved = (conn.recv(1024)).decode('UTF-8')
            data = yaml.safe_load(recieved)
            if not data:
                break
            #if data[1]==1 -> write data[0] to csv
            if data[1]==1:
                #create File with fields or check if its there
                createCSV('plop.csv')
                #write data[0] to filename
                affirm = writeCSV(data[0], 'plop.csv')
                print(affirm)
            elif data[1]==2: #else if data[2]==1 -> make id==data[0] query
                affirm = str(readCSV(str(data[0]), 'plop.csv'))

            print(f"        data: {data}\ntype of data: {type(data)}")

            #Send bytes
            conn.sendall(bytes(affirm, 'UTF-8'))
