#!/usr/bin/env python3

import socket
import pickle

HOST = '0.0.0.0'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('connected by', addr)
        while True:
            data = pickle.loads(conn.recv(1024))
            print(repr(data))
            if not data:
                break
            conn.sendall(data)
