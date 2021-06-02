import socket
import enum
import struct
from collections import deque



HDR_SIZE = 4
MAGIC = 0x1FEA
SYN = 0x8000
ACK = 0x4000
FIN = 0x2000

SYN_HDR = SYN & MAGIC
SYNACK_HDR = SYN & ACK & MAGIC
ACK_HDR = ACK & MAGIC


class state(enum.Enum):
    INIT = 0
    READY = 1
    WAIT_FOR_SYN = 2
    WAIT_FOR_ACK = 3

class virtual_socket:
    def __init__(self, server_sock, dst_ip, dst_port, src_ip, src_port):
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.src_ip = src_ip
        self.src_port = src_port
        self.server_sock = server_sock
        self.buf = deque()
    def send(self, msg):
        self.server_sock.sock.sendto(msg, (self.dst_ip, self.dst_port))
    def recv(self, size):
        while not (self.buf):
            self.server_sock.recv(size)
        return self.buf.popleft()
    def copy_data_to_buf(self, data):
        self.buf.append(data)
    def close(self):
        return

class server_socket:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.established_connections = {}
        self.src_ip = None
        self.src_port = None
        self.state = state.INIT 
        self.max_conn = 0
        self.num_conn = 0
    def bind(self, *saddr):
        addr = saddr[0]
        self.sock.bind(addr)
        self.src_ip = addr[0]
        self.src_port = addr[1]
    def listen(self, num):
        self.max_conn = num
        self.set_state(state.READY)
    def set_state(self, state):
        print("Server State: %s -> %s" % (self.state, state))
        self.state = state
    def chk_msg(self, msg, addr):
        if self.state == state.WAIT_FOR_SYN:
            if msg.decode() == str(SYN_HDR):
                print ("Got SYN msg")
                key = (addr[0], addr[1], self.src_ip, self.src_port)
                if self.max_conn > self.num_conn and not key in self.established_connections:
                    self.set_state(state.WAIT_FOR_ACK)
                    send_msg = str(SYNACK_HDR)
                    self.sock.sendto(send_msg.encode(), addr)
                else:
                    print ("Connection request is refused")
            return 0
        elif self.state == state.WAIT_FOR_ACK:
            if msg.decode() == str(ACK_HDR):
                print ("Got ACK msg")
                key = (addr[0], addr[1], self.src_ip, self.src_port)
                if not key in self.established_connections:
                    self.established_connections[key] = virtual_socket(self, addr[0], addr[1], self.src_ip, self.src_port);
                    self.num_conn += 1
                    self.set_state(state.READY)
                    print ("Connection Established: ", key)
                    return 1
                return 0
            return 0
        else:
            return 0
    def accept(self):
        connected = 0
        self.set_state(state.WAIT_FOR_SYN)
        while (connected == 0):
            recv_msg, addr = self.sock.recvfrom(32)
            connected = self.chk_msg(recv_msg, addr)
        key = (addr[0], addr[1], self.src_ip, self.src_port)
        return (self.established_connections[key], addr)

    def recv(self, size):
        msg, addr = self.sock.recvfrom(size)
        key = (addr[0], addr[1], self.src_ip, self.src_port)
        if (key in self.established_connections):
            vsock = self.established_connections[key]
            vsock.copy_data_to_buf(msg)
        else:
            print("something wrong")
    def close(self):
        self.sock.close()

class client_socket:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dst_ip = None
        self.dst_port = None
        self.src_ip = None
        self.src_port = None
        self.connected = 0
    def connect(self, *addr):
        self.dst_ip = addr[0]
        self.dst_port = addr[1]
        message = str(SYN_HDR)
        self.sock.sendto(message.encode(), (self.dst_ip, self.dst_port))
        while (self.connected == 0):
            recv_msg, addr = self.sock.recvfrom(32)
            if recv_msg.decode() == str(SYNACK_HDR):
                message = str(ACK_HDR)
                self.sock.sendto(message.encode(), addr)
                self.connected = 1
    def send(self, msg):
        self.sock.sendto(msg, (self.dst_ip, self.dst_port))
    def recv(self, size):
        return self.sock.recv(size)
    def close(self):
        self.sock.close()
    
