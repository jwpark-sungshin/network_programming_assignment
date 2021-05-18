import socket
import enum
import struct
from collections import deque


MAGIC = 0x1FEA
SYN = 0x8000
ACK = 0x4000
FIN = 0x2000

SYN_HDR = SYN & MAGIC
SYNACK_HDR = SYN & ACK & MAGIC
ACK_HDR = ACK & MAGIC

class state(enum.Enum):  # Server state
    INIT = 0
    READY = 1
    WAIT_FOR_SYN = 2
    WAIT_FOR_ACK = 3

class virtual_socket: # 서버 쪽에서 accept()을 호출할 경우 생성되는 소켓 이후 클라이언트와의 통신에 활용됨
    def __init__(self, server_sock, dst_ip, dst_port, src_ip, src_port):
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.src_ip = src_ip
        self.src_port = src_port
        self.server_sock = server_sock
        self.buf = deque() # deque를 virtual socket의 임시저장소로 활용
    def send(self, msg):
        # 서버 쪽에서 virtual socket을 통해 연결된 클라이언트에게 메세지를 보낼 때 활용
        self.server_sock.sock.sendto(msg, (self.dst_ip, self.dst_port))
    def recv(self, size):
        # 연결된 클라이언트가 보낸 메세지가 있을 경우 전달
        # 내 virtual socket의 buf에 쌓여있는 메세지가 있으면, 메세지 리턴
        # 없으면? server_socket의 recv 함수 호출
        # 언제까지?
        # 구현할 것




        #############################################################

    def copy_data_to_buf(self, data):
        # 메세지를 내 buf에 추가
        # 구현할 것



        #############################################################

    def close(self):
        return

class server_socket: # 서버쪽에서 클라이언트의 연결 요청을 받기 위해 생성하는 소켓
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.established_connections = {} # 연결이 이루어진 서버 클라이언트 조합을 저장
        self.src_ip = None
        self.src_port = None
        self.state = state.INIT # 서버의 상태 변화
        self.max_conn = 0
        self.num_conn = 0
    def bind(self, *saddr): # server socket이 특정 IP 주소, Port 넘버에 바인드하도록 설정
        addr = saddr[0]
        self.sock.bind(addr)
        self.src_ip = addr[0]
        self.src_port = addr[1]
    def listen(self, num): # server socket이 최대 몇 개의 연결을 받아들일 수 있는지를 설정
        self.max_conn = num
        self.set_state(state.READY)
    def set_state(self, state): # 서버의 상태 변경
        print("Server State: %s -> %s" % (self.state, state))
        self.state = state
    def chk_msg(self, msg, addr): # 연결을 기다리는 상황에서 클라이언트로부터 전달받은 메세지를 처리, 연결이 이루어졌으면 1을 리턴
        if self.state == state.WAIT_FOR_SYN:
            if msg.decode() == str(SYN_HDR):
                print ("Got SYN msg")
                # 클라이언트가 보낸 메세지가 SYN 메세지면,
                # 최대 연결 수를 참고하여 추가 연결이 가능한지 확인
                # 이미 연결이 이루어진 상태인지 established_connections에서 확인
                # 서버 상태 변경
                # 클라이언트에게 SYNACK 메세지 보냄
                # 구현할 것



                ######################################################
            return 0
        elif self.state == state.WAIT_FOR_ACK:
            if msg.decode() == str(ACK_HDR):
                print ("Got ACK msg")
                # 클라이언트가 보낸 메세지가 ACK 메세지면,
                # 이미 연결이 이루진 상태인지 established_connections에서 확인
                # 새로운 virtual socket 생성
                # established_connections에 (dst IP, dst port, src IP, src port) -> virtual socket 맵핑을 저장
                # 서버 상태 변경
                # 구현할 것




                ############################################################
            return 0
        else:
            return 0
    def accept(self): # 클라이언트로부터 연결 요청이 올 때까지 대기 후 연결
        connected = 0
        self.set_state(state.WAIT_FOR_SYN)
        while (connected == 0):
            recv_msg, addr = self.sock.recvfrom(32)
            connected = self.chk_msg(recv_msg, addr)
        key = (addr[0], addr[1], self.src_ip, self.src_port)
        return (self.established_connections[key], addr)

    def recv(self, size): # server socket이 대표로 UDP 메세지를 수신
        msg, addr = self.sock.recvfrom(size)
        # 전달받은 메세지를 적절한 virtual socket의 buf에 저장
        # 구현할 것






        ###############################################################

    def close(self):
        self.sock.close()

class client_socket: # 클라이언트에서 통신을 위해 생성하는 소켓
    def __init__(self): 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dst_ip = None
        self.dst_port = None
        self.src_ip = None
        self.src_port = None
        self.connected = 0
    def connect(self, *addr): # 서버 쪽에 연결 요청
        self.dst_ip = addr[0]
        self.dst_port = addr[1]
        message = str(SYN_HDR)
        # 연결이 될 때까지 서버와 메세지를 주고 받음 3-way handshaking
        # 구현할 것





        ########################################################
    def send(self, msg):
        self.sock.sendto(msg, (self.dst_ip, self.dst_port))
    def recv(self, size):
        return self.sock.recv(size)
    def close(self):
        self.sock.close()
