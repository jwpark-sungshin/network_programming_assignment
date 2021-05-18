import coudp
import threading
import time

HOST = '127.0.0.1'
PORT = 5005 

def client_program():
    client_sock = coudp.client_socket()
    client_sock.connect(HOST, PORT)
    client_sock2 = coudp.client_socket()
    client_sock2.connect(HOST, PORT)
    client_sock3 = coudp.client_socket()
    client_sock3.connect(HOST, PORT)
    for i in range(10):
        client_sock.send("Message %d from client1".encode() % i)
        if i % 2 == 0:
            client_sock2.send("Message %d from client2".encode() % i)
        if i % 3 == 0:
            client_sock3.send("Message %d from client3".encode() % i)
    client_sock.close()
    client_sock2.close()
    client_sock3.close()

def server_program():
    server_sock = coudp.server_socket()
    server_sock.bind((HOST, PORT))
    server_sock.listen(10)
    sock1, client1_addr = server_sock.accept()
    sock2, client2_addr = server_sock.accept()
    sock3, client3_addr = server_sock.accept()

    for i in range(10):
        print ("Socket 1: ", sock1.recv(1024).decode())
    for i in range(0,10,2):
        print ("Socket 2: ", sock2.recv(1024).decode())
    for i in range(0,10,3):
        print ("Socket 3: ", sock3.recv(1024).decode())
    sock1.close()
    sock2.close()
    sock3.close()
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
