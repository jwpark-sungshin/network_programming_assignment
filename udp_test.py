import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 5005 

def client_program():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(10):
        client_sock.sendto("Message %d from client1".encode() % i, (HOST, PORT))
        if i % 2 == 0:
            client_sock2.sendto("Message %d from client2".encode() % i, (HOST, PORT))
        if i % 3 == 0:
            client_sock3.sendto("Message %d from client3".encode() % i, (HOST, PORT))
    client_sock.close()
    client_sock2.close()
    client_sock3.close()

def server_program():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind((HOST, PORT))

    for i in range(10):
        print ("Socket 1: ", server_sock.recv(1024).decode())
    for i in range(0,10,2):
        print ("Socket 1: ", server_sock.recv(1024).decode())
    for i in range(0,10,3):
        print ("Socket 1: ", server_sock.recv(1024).decode())
    server_sock.close()


try:
    server = threading.Thread(target=server_program)
    client = threading.Thread(target=client_program)
    server.start()
    time.sleep(1)
    client.start()
    client.join()
    server.join()
except:
    print ("Error: unable to start thread")
